
import pandas as pd
import numpy as np
import pulp
import math

# Read the input data
file_path = "Corrected_Rajshahi_STS_Coordinates.xlsx"

df_nodes = pd.read_excel(file_path, sheet_name="Cluster sts")
df_nodes["STS Name"] = df_nodes["STS Name"].astype(str).str.strip()

sts = df_nodes["STS Name"].tolist()
depot = "Nawhata Landfill (Depot)"
nodes = [depot] + sts

# Distance between the depot and STSs, and between STSs
df_dist = pd.read_excel(
    file_path,
    sheet_name="Distance Matrix",
    index_col=0
)

df_dist.index = df_dist.index.astype(str).str.strip()
df_dist.columns = df_dist.columns.astype(str).str.strip()

dist = {}
for i in nodes:
    for j in nodes:
        if i in df_dist.index and j in df_dist.columns:
            dist[i, j] = float(df_dist.loc[i, j])
        else:
            dist[i, j] = 0.0

# Daily waste generation data
df_waste = pd.read_excel(
    file_path,
    sheet_name="Simulated_Waste",
    index_col="STS Name"
)

df_waste.index = df_waste.index.astype(str).str.strip()
waste_column = df_waste.columns[0]

# Model parameters
beta = 1.4
v = 20.0
t_LU = 0.5
T_max = 8.0
lam = 3.85
Big_M = 100.0
Gamma = 0.20

# Vehicle types and their characteristics
K_S = ["Type 3 (5.0T)"]
K_R_base = "Type 2 (3.0T)"

Q = {
    K_S[0]: 5.0,
    K_R_base: 3.0
}

Cfuel = {
    K_S[0]: 35.0,
    K_R_base: 25.0
}

Cwage = {
    K_S[0]: 1800,
    K_R_base: 1500
}

Ekem = {
    K_S[0]: 0.35,
    K_R_base: 0.22
}

# Adjust waste demand using the selected demand scenario
demand = {}
for i in sts:
    if i in df_waste.index:
        demand[i] = float(df_waste.loc[i, waste_column]) * (1 + Gamma)
    else:
        demand[i] = 0.0

# Service time windows
E_i = {i: 8.0 for i in sts}
L_i = {i: 16.0 for i in sts}

# Travel time after considering traffic congestion
travel_time = {
    (i, j): dist[i, j] / (v / beta)
    for i in nodes for j in nodes
}

# Estimate the number of sweepers needed for the total leftover waste
leftover = sum(
    max(
        0.0,
        demand[i] -
        max(1, math.floor(demand[i] / Q[K_S[0]])) * Q[K_S[0]]
    )
    for i in sts
)

needed_sweepers = max(
    1,
    math.ceil(leftover / Q[K_R_base])
) + 1

K_R = [
    f"{K_R_base}_#{n}"
    for n in range(1, needed_sweepers + 1)
]

# Assign the same characteristics to each sweeper
for k in K_R:
    Q[k] = Q[K_R_base]
    Cfuel[k] = Cfuel[K_R_base]
    Cwage[k] = Cwage[K_R_base]
    Ekem[k] = Ekem[K_R_base]

# Each sweeper is allowed to make two trips
M = [1, 2]

arcs = [(i, j) for i in nodes for j in nodes if i != j]
N_sts = len(sts)

# Set up the optimization model
model = pulp.LpProblem(
    "Waste_Collection_Routing",
    pulp.LpMinimize
)

# Decision variables
y = pulp.LpVariable.dicts(
    "y",
    ((i, k) for i in sts for k in K_S),
    lowBound=0,
    cat="Integer"
)

x = pulp.LpVariable.dicts(
    "x",
    ((i, j, k, m) for i, j in arcs for k in K_R for m in M),
    cat="Binary"
)

q = pulp.LpVariable.dicts(
    "q",
    ((i, k, m) for i in sts for k in K_R for m in M),
    lowBound=0
)

T_var = pulp.LpVariable.dicts(
    "T",
    ((i, k, m) for i in nodes for k in K_R for m in M),
    lowBound=0
)

u = pulp.LpVariable.dicts(
    "u",
    ((i, k, m) for i in sts for k in K_R for m in M),
    lowBound=1,
    upBound=N_sts
)

Nk = pulp.LpVariable.dicts(
    "Nk",
    K_S + K_R,
    lowBound=0,
    cat="Integer"
)

# Calculate transportation and vehicle costs
Z_shuttle = pulp.lpSum(
    (beta * Cfuel[k] + lam * Ekem[k])
    * 2 * dist[depot, i] * y[i, k]
    for i in sts for k in K_S
)

Z_sweeper = pulp.lpSum(
    (beta * Cfuel[k] + lam * Ekem[k])
    * dist[i, j] * x[i, j, k, m]
    for i, j in arcs for k in K_R for m in M
)

Z_wage = pulp.lpSum(
    Cwage[k] * Nk[k]
    for k in K_S + K_R
)

model += Z_shuttle + Z_sweeper + Z_wage

# Ensure that every STS receives at least one shuttle trip
for i in sts:
    model += pulp.lpSum(y[i, k] for k in K_S) >= 1

    # The combined collection capacity must meet the waste demand
    model += (
        pulp.lpSum(Q[k] * y[i, k] for k in K_S)
        + pulp.lpSum(q[i, k, m] for k in K_R for m in M)
        >= demand[i]
    )

    # Limit the number of shuttle trips according to demand
    for k in K_S:
        model += y[i, k] <= math.ceil(demand[i] / Q[k])

# Routing and collection constraints for sweepers
for k in K_R:
    for m in M:

        # Incoming and outgoing routes must balance at each node
        for i in nodes:
            model += (
                pulp.lpSum(x[i, j, k, m] for j in nodes if i != j)
                ==
                pulp.lpSum(x[j, i, k, m] for j in nodes if i != j)
            )

        # A sweeper can leave the depot only once per trip
        depot_depart = pulp.lpSum(
            x[depot, j, k, m] for j in sts
        )
        model += depot_depart <= 1

        # Waste can only be collected from a visited STS
        for i in sts:
            model += (
                q[i, k, m]
                <= Q[k] * pulp.lpSum(
                    x[i, j, k, m] for j in nodes if i != j
                )
            )

        # Total collected waste cannot exceed vehicle capacity
        model += (
            pulp.lpSum(q[i, k, m] for i in sts)
            <= Q[k] * depot_depart
        )

        # Prevent subtours among STSs using MTZ constraints
        for i in sts:
            for j in sts:
                if i != j:
                    model += (
                        u[i, k, m] - u[j, k, m]
                        + N_sts * x[i, j, k, m]
                        <= N_sts - 1
                    )

        # Apply the service time window at each visited STS
        for i in sts:
            visit = pulp.lpSum(
                x[i, j, k, m] for j in nodes if i != j
            )

            model += T_var[i, k, m] >= E_i[i] * visit
            model += T_var[i, k, m] <= L_i[i] * visit

        # Maintain the correct arrival time along each route
        for i, j in arcs:
            if j != depot:
                model += (
                    T_var[j, k, m]
                    >= T_var[i, k, m]
                    + travel_time[i, j] + t_LU
                    - Big_M * (1 - x[i, j, k, m])
                )

        # Keep each trip within the maximum working time
        model += pulp.lpSum(
            (travel_time[i, j] + t_LU) * x[i, j, k, m]
            for i, j in arcs
        ) <= T_max

    # Estimate the number of sweepers from the total assigned trips
    model += (
        Nk[k]
        >= pulp.lpSum(
            x[depot, j, k, m]
            for j in sts for m in M
        ) / len(M)
    )

# Calculate the required number of shuttle vehicles
for k in K_S:
    model += (
        Nk[k] >= pulp.lpSum(y[i, k] for i in sts) / 5.0
    )

# Symmetry-breaking constraint for identical sweeper vehicles
if len(K_R) > 1:
    for n in range(len(K_R) - 1):
        model += (
            pulp.lpSum(x[depot, j, K_R[n], 1] for j in sts)
            >=
            pulp.lpSum(x[depot, j, K_R[n + 1], 1] for j in sts)
        )

# Solve the model
model.solve(
    pulp.GUROBI_CMD(
        msg=True,
        timeLimit=120,
        options=[("MIPGap", 0.05)]
    )
)

# Display the optimization results
print("Solver status:", pulp.LpStatus[model.status])

if model.status == pulp.LpStatusOptimal:

    print("Minimum operational cost:",
          round(pulp.value(model.objective), 2))

    print("\nRequired vehicles:")
    for k in K_S + K_R:
        print(k, ":", pulp.value(Nk[k]))

    print("\nShuttle allocation:")
    for i in sts:
        for k in K_S:
            trips = pulp.value(y[i, k])
            if trips is not None and trips > 0:
                print(i, "-", trips, "trips")

    print("\nSweeper routes:")
    for k in K_R:
        for m in M:
            route = [depot]
            current = depot
            visited = set()

            while True:
                next_nodes = [
                    j for j in sts
                    if pulp.value(x[current, j, k, m]) is not None
                    and pulp.value(x[current, j, k, m]) > 0.5
                    and j not in visited
                ]

                if not next_nodes:
                    if current != depot:
                        if pulp.value(x[current, depot, k, m]) > 0.5:
                            route.append(depot)
                    break

                next_node = next_nodes[0]
                route.append(next_node)
                visited.add(next_node)
                current = next_node

            if len(route) > 1:
                print(f"{k}, Trip {m}: {' -> '.join(route)}")

else:
    print("The solver did not find a proven optimal solution.")
