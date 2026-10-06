from flask import Flask, render_template, request, redirect, url_for
import networkx as nx
import matplotlib.pyplot as plt
import os
from collections import deque

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

network = {}
capacities = {}
graph = {}


def bfs_migration_path(start_node, job_id):
    visited = set()
    queue = deque([(start_node, [])])

    while queue:
        current_node, path = queue.popleft()
        visited.add(current_node)

        if len(network[current_node]) < capacities[current_node]:
            network[current_node].append(job_id)
            return path + [current_node]  # Return path including destination

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [current_node]))

    return []  # No valid migration path found


def draw_network(migration_path=None):
    G = nx.Graph()
    G.add_nodes_from(network.keys())

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G)
    node_colors = []
    edge_colors = []

    for node in G.nodes():
        if migration_path and node in migration_path:
            node_colors.append('orange')  # Highlight migration path nodes
        else:
            node_colors.append('lightblue')

    for edge in G.edges():
        if migration_path and (edge[0] in migration_path and edge[1] in migration_path):
            edge_colors.append('orange')  # Highlight migration path edges
        else:
            edge_colors.append('lightgrey')

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)

    labels = {node: f"{node}\n({len(network[node])}/{capacities[node]})" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    plt.title("Network Configuration & Migration Path")

    filename = "network_migration.png"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    plt.savefig(path)
    plt.close()
    return filename


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/network-config', methods=['GET', 'POST'])
def network_config():
    if request.method == 'POST':
        global network, capacities, graph
        network = {}
        capacities = {}
        graph = {}

        nodes_input = request.form['nodes'].strip().split('\n')

        # Step 1: Collect all jobs and nodes to check for duplicates
        all_jobs = set()
        all_nodes = {}
        job_repeats = {}
        node_repeats = {}

        for line in nodes_input:
            parts = line.strip().split()
            if len(parts) >= 2:
                node_id = parts[0]
                capacity = int(parts[1])
                jobs = parts[2].split(',') if len(parts) == 3 and parts[2] else []

                # Check for duplicate jobs
                for job in jobs:
                    if job in all_jobs:
                        job_repeats[job] = job_repeats.get(job, 0) + 1
                    all_jobs.add(job)

                # Check for duplicate nodes
                if node_id in all_nodes:
                    node_repeats[node_id] = node_repeats.get(node_id, 0) + 1
                all_nodes[node_id] = capacity

                network[node_id] = jobs
                capacities[node_id] = capacity

        # Check if there are any repeated jobs or nodes
        if job_repeats:
            job_msg = "Job(s) repeated: " + ", ".join([f"{job} ({count} times)" for job, count in job_repeats.items()])
            return render_template('network_config.html', message=f"⚠️ {job_msg}. Cannot set up the network!")

        if node_repeats:
            node_msg = "Node(s) repeated: " + ", ".join(
                [f"{node} ({count} times)" for node, count in node_repeats.items()])
            return render_template('network_config.html', message=f"⚠️ {node_msg}. Cannot set up the network!")

        edges_input = request.form['edges'].strip().split('\n')
        for line in edges_input:
            node1, node2 = line.strip().split()
            graph.setdefault(node1, []).append(node2)
            graph.setdefault(node2, []).append(node1)

        return redirect(url_for('submit_job'))

    return render_template('network_config.html')


@app.route('/submit-job', methods=['GET', 'POST'])
def submit_job():
    message = ""
    image_path = None

    if request.method == 'POST':
        node_id = request.form['node_id'].strip()
        job_id = request.form['job_id'].strip()

        # Check if the job already exists in any node
        job_exists = any(job_id in jobs for jobs in network.values())

        if job_exists:
            message = f"⚠️ Job {job_id} is already assigned to a node! A job can only be allocated once in the entire network."
        elif node_id not in network:
            message = f"❌ Node {node_id} does not exist."
        else:
            if len(network[node_id]) < capacities[node_id]:
                network[node_id].append(job_id)
                message = f"✅ Job {job_id} successfully added to {node_id}."
                image_path = draw_network()
            else:
                migration_path = bfs_migration_path(node_id, job_id)
                if migration_path:
                    destination = migration_path[-1]
                    message = f"⚠️ {node_id} is full. Job {job_id} migrated to {destination} via path: {' ➡️ '.join(migration_path)}"
                    image_path = draw_network(migration_path)
                else:
                    message = f"❌ No vacancies available for Job {job_id}, all nodes are full."
                    image_path = draw_network()

    return render_template('submit_jobs.html', message=message, network=network,
                           capacities=capacities, graph=graph, image_path=image_path)


if __name__ == '__main__':
    app.run(debug=True)
