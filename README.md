🗺️ NIT Patna Campus Navigation System

An interactive campus navigation system built using Python that models the NIT Patna campus as a weighted graph. The system calculates the shortest route between campus locations using Dijkstra’s Algorithm and visualizes the results on an interactive map.

🚀 Features

📍 Models campus locations as graph nodes

🛣️ Defines paths as weighted edges (distance in meters)

🧠 Implements Dijkstra’s Algorithm for shortest path calculation

🗺️ Generates interactive maps using Folium

🎯 Highlights start and end points

🔵 Visually displays the shortest route

🌐 Automatically opens map in browser

🛠️ Technologies Used

Programming Language: Python

Libraries:

NetworkX (Graph creation and pathfinding)

Folium (Interactive map visualization)

Webbrowser (Auto-launch map)

OS (File handling)

🧠 Concepts Applied

Graph Theory

Dijkstra’s Algorithm

Weighted Graphs

Shortest Path Algorithms

Geographic Mapping

Data Structures

📊 How It Works

Campus locations are stored as graph nodes with GPS coordinates.

Paths between locations are added as weighted edges.

Dijkstra’s Algorithm computes the minimum distance path.

Folium generates an interactive HTML map.

The shortest path is highlighted in blue.

📂 Project Structure
Campus-Navigation-System/
│── main.py
│── nitp_full_map_ashokrajpath.html
│── nitp_path_gate_to_canteen.html
│── README.md
