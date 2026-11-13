
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Load the STS information from the Excel file
excel_file = "Corrected_Rajshahi_STS_Coordinates.xlsx"

df_nodes = pd.read_excel(excel_file, sheet_name="Cluster sts")

# Remove any extra spaces from the STS names
df_nodes['STS Name'] = df_nodes['STS Name'].astype(str).str.strip()

# Get the geographical coordinates of all STSs
sts_coordinates = df_nodes[['Latitude', 'Longitude']].values

# Divide the STSs into four clusters based on their locations
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)

# Assign a cluster number to each STS
df_nodes['Cluster_ID'] = kmeans.fit_predict(sts_coordinates)

# Group the STS names according to their assigned clusters
clusters = {}

for _, row in df_nodes.iterrows():
    cluster_id = row['Cluster_ID']
    sts_name = row['STS Name']

    if cluster_id not in clusters:
        clusters[cluster_id] = []

    clusters[cluster_id].append(sts_name)

# Display the STSs belonging to each cluster
for cluster_id, sts_list in sorted(clusters.items()):
    print(f"\nCluster {cluster_id}:")
    for sts in sts_list:
        print(f"  - {sts}")

# Save the clustering results for further analysis
df_nodes.to_csv("STS_Clustering_Results.csv", index=False)

print("\nClustering completed successfully!")
print(f"Total STSs: {len(df_nodes)}")
print(f"Number of clusters: {len(clusters)}")
