# -*- coding: utf-8 -*-
"""
Created on Tue Feb 4 20:39:25 2025

@author: IAN CARTER KULANI

"""

import random
import tkinter as tk
from tkinter import messagebox

# A simple class for representing a node in the FANET
class Node:
    def __init__(self, node_id, position):
        self.node_id = node_id
        self.position = position  # (x, y) coordinates
        self.routing_table = {}  # Stores known routes {destination: (next_hop, hops)}

    def add_route(self, destination, next_hop, hops):
        self.routing_table[destination] = (next_hop, hops)
    
    def delete_route(self, destination):
        if destination in self.routing_table:
            del self.routing_table[destination]
    
    def get_route(self, destination):
        return self.routing_table.get(destination, None)

# A function to simulate the AODV route discovery process
def route_discovery(source, destination, nodes, output_text):
    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, f"Node {source.node_id} is trying to discover a route to Node {destination.node_id}.\n")

    # Simulate broadcasting a Route Request (RREQ)
    visited_nodes = set()
    rreq_queue = [source]
    
    while rreq_queue:
        current_node = rreq_queue.pop(0)
        output_text.insert(tk.END, f"Node {current_node.node_id} broadcasting RREQ.\n")
        output_text.yview(tk.END)  # Auto-scroll to the latest message
        
        # Check if we have already visited this node
        if current_node.node_id in visited_nodes:
            continue
        visited_nodes.add(current_node.node_id)

        # Check if current node is the destination
        if current_node.node_id == destination.node_id:
            output_text.insert(tk.END, f"Destination Node {destination.node_id} reached!\n")
            output_text.insert(tk.END, f"Route found via Node {current_node.node_id}.\n")
            return

        # Propagate RREQ to neighboring nodes (simulated by checking all other nodes)
        for neighbor in nodes:
            if neighbor != current_node and neighbor.node_id not in visited_nodes:
                rreq_queue.append(neighbor)

    output_text.insert(tk.END, "Route discovery failed. No route found.\n")
    output_text.yview(tk.END)  # Auto-scroll to the latest message

# Function to handle the user input and start the route discovery
def start_simulation():
    try:
        num_nodes = int(num_nodes_entry.get())
        if num_nodes <= 0:
            raise ValueError("Number of nodes must be greater than 0.")
        
        # Create the nodes with random positions (x, y)
        nodes = []
        for i in range(num_nodes):
            position = (random.randint(0, 100), random.randint(0, 100))  # Random positions
            nodes.append(Node(i, position))
        
        source_id = int(source_entry.get())
        destination_id = int(destination_entry.get())

        if source_id < 0 or source_id >= num_nodes or destination_id < 0 or destination_id >= num_nodes:
            raise ValueError("Source or destination node ID is out of range.")

        source_node = nodes[source_id]
        destination_node = nodes[destination_id]
        
        # Start the route discovery process and display in the text widget
        route_discovery(source_node, destination_node, nodes, output_text)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Creating the main window
root = tk.Tk()
root.title("FANET Routing Simulation (AODV-like)")

# Set window size
root.geometry("600x400")

# Creating labels and entry widgets for user inputs
tk.Label(root, text="Enter the number of nodes in the FANET:").pack(pady=5)
num_nodes_entry = tk.Entry(root)
num_nodes_entry.pack(pady=5)

tk.Label(root, text="Enter the source node ID:").pack(pady=5)
source_entry = tk.Entry(root)
source_entry.pack(pady=5)

tk.Label(root, text="Enter the destination node ID:").pack(pady=5)
destination_entry = tk.Entry(root)
destination_entry.pack(pady=5)

# Button to start the simulation
start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.pack(pady=20)

# Creating a Text widget to display the output (routing process)
output_text = tk.Text(root, width=70, height=10)
output_text.pack(pady=10)

# Run the application
root.mainloop()
