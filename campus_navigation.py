import networkx as nx
import folium
import webbrowser
import os

# --- 1. Campus Data (CORRECTED for NIT Patna - Ashok Rajpath Location) ---
# Verified coordinates for the NIT Patna main campus on Ashok Rajpath.
locations = {
    'Main Gate': {
        'pos': (25.620500, 85.171800), # Ashok Rajpath Entrance
        'info': 'Main entrance to the campus (Ashok Rajpath).'
    },
    'Admin Building': {
        'pos': (25.621100, 85.172200), # Central Administrative offices
        'info': 'Administrative offices and Director\'s office.'
    },
    'CSE Department': {
        'pos': (25.620900, 85.172200), # Computer Science and Engineering building (part of main cluster)
        'info': 'Computer Science and Engineering building.'
    },
    'Central Library': {
        'pos': (25.621250, 85.172300), # The central library
        'info': 'The central library of NIT Patna.'
    },
    'Main Canteen': {
        'pos': (25.620700, 85.172100), # Main food court
        'info': 'Main food court for students.'
    },
    'Sone Hostel': {
        'pos': (25.620400, 85.172000), # Boys' Hostel area
        'info': 'Boys\' Hostel block (Sone Hostel).'
    },
    'Sports Ground': {
        'pos': (25.621000, 85.172550), # East side, near Gandhi Ghat/River bank
        'info': 'The main sports and athletics field.'
    }
}

# Define the paths between locations with approximate distances in meters.
# Distances are revised to better reflect the compact Ashok Rajpath campus.
paths = [
    ('Main Gate', 'Admin Building', 100), # Closer path
    ('Admin Building', 'CSE Department', 50), # Very short distance within cluster
    ('Admin Building', 'Sports Ground', 150),
    ('CSE Department', 'Central Library', 70),
    ('Central Library', 'Main Canteen', 100),
    ('Main Canteen', 'Sone Hostel', 80),
    ('Sports Ground', 'Central Library', 120),
    ('Sports Ground', 'Main Gate', 180) # Longer path around the perimeter
]

# --- 2. Create the Campus Graph ---
G = nx.Graph()

# Add nodes (locations) from the dictionary
for location, data in locations.items():
    G.add_node(location, pos=data['pos'], info=data['info'])

# Add edges (paths) with weights (distances)
for path in paths:
    G.add_edge(path[0], path[1], weight=path[2])

# --- 3. Core Functions (Pathfinding and Plotting - No logic changes needed) ---

def plot_university_map(graph, map_center, zoom=18, map_file="nitp_full_map_ashokrajpath.html"):
    """Creates and saves an interactive Folium map of the campus."""
    campus_map = folium.Map(location=map_center, zoom_start=zoom)

    # Add markers for each location
    for node, data in graph.nodes(data=True):
        lat, lon = data['pos']
        info = data['info']
        popup_text = f"<b>{node}</b><br>{info}"
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=200),
            tooltip=node,
            icon=folium.Icon(color='blue', icon='university', prefix='fa')
        ).add_to(campus_map)

    # Add lines for each path
    for start_node, end_node in graph.edges():
        pos1 = graph.nodes[start_node]['pos']
        pos2 = graph.nodes[end_node]['pos']
        folium.PolyLine(locations=[pos1, pos2], color='gray', weight=2.5, opacity=1).add_to(campus_map)

    campus_map.save(map_file)
    print(f"✅ Full campus map saved as '{map_file}'")
    webbrowser.open('file://' + os.path.realpath(map_file))

def find_and_plot_shortest_path(graph, start_loc, end_loc, map_file="nitp_path_ashokrajpath.html"):
    """Finds the shortest path and plots it on a new map."""
    if start_loc not in graph or end_loc not in graph:
        print("❌ Error: One or both locations not found on the map.")
        return

    try:
        shortest_path = nx.dijkstra_path(graph, source=start_loc, target=end_loc, weight='weight')
        path_length = nx.dijkstra_path_length(graph, source=start_loc, target=end_loc, weight='weight')
        print(f"📍 Shortest Path from {start_loc} to {end_loc}: {' -> '.join(shortest_path)}")
        print(f"📏 Total Distance: {path_length:.2f} meters")

        start_pos = graph.nodes[start_loc]['pos']
        end_pos = graph.nodes[end_loc]['pos']
        map_center = [(start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2]
        path_map = folium.Map(location=map_center, zoom_start=18)

        # Add all nodes and edges for context
        for node, data in graph.nodes(data=True):
            folium.Marker(location=data['pos'], tooltip=node, icon=folium.Icon(color='gray')).add_to(path_map)
        for u, v in graph.edges():
            folium.PolyLine(locations=[graph.nodes[u]['pos'], graph.nodes[v]['pos']], color='lightgray', weight=2).add_to(path_map)

        # Highlight start and end markers
        folium.Marker(location=start_pos, popup=f"<b>START: {start_loc}</b>", icon=folium.Icon(color='green', icon='play')).add_to(path_map)
        folium.Marker(location=end_pos, popup=f"<b>END: {end_loc}</b>", icon=folium.Icon(color='red', icon='stop')).add_to(path_map)

        # Draw the shortest path
        path_points = [graph.nodes[node]['pos'] for node in shortest_path]
        folium.PolyLine(locations=path_points, color='blue', weight=5, opacity=0.8).add_to(path_map)

        path_map.save(map_file)
        print(f"✅ Path map saved as '{map_file}'")
        webbrowser.open('file://' + os.path.realpath(map_file))

    except nx.NetworkXNoPath:
        print(f"❌ No path found between {start_loc} and {end_loc}.")

# --- 4. Main Execution ---
if __name__ == "__main__":
    # --- Part A: Plot the entire NIT Patna campus map ---
    print("--- 🗺 Generating Full NIT Patna Campus Map (Ashok Rajpath) ---")
    # Center the map on a central location like the Admin Building
    map_center_coords = locations['Admin Building']['pos']
    plot_university_map(G, map_center=map_center_coords)
    
    print("\n" + "="*50 + "\n")

    # --- Part B: Find and plot the shortest path between two points ---
    print("--- 📍 Calculating Shortest Path ---")
    # Find the shortest path from the Main Gate to the Main Canteen
    start_location = 'Main Gate'
    end_location = 'Main Canteen'
    find_and_plot_shortest_path(G, start_location, end_location, map_file="nitp_path_gate_to_canteen.html")