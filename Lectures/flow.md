# Flow

## I. Introduction to Flow Networks

### I. Introduction to Flow Networks

**Definition of a Flow Network**

A **flow network** is formally defined as a tuple $ N = (G, c, s, t) $, where:

- $ G = (V, E) $ is a directed graph consisting of:
  - A set of vertices $ V $
  - A set of directed edges $ E $
  - $ c: E \rightarrow \mathbb{R}_0^+ $ is a capacity function that assigns a non-negative real number to each edge, denoting the maximum flow that can pass through that edge.
- $ s \in V $ is the **source**, the vertex where flow originates.
- $ t \in V $ is the **sink**, the vertex where flow is intended to terminate.

An admissible flow $ f $ on the network is defined as a mapping $ f: E \rightarrow \mathbb{R}_0^+ $ satisfying two main constraints:

1. **Capacity Constraint**: For every edge $ e \in E $,
   $$
   0 \leq f(e) \leq c(e)
   $$
   This means that the flow through each edge cannot exceed its capacity.

2. **Flow Conservation**: For every vertex $ v \neq s, t $,
   $$
   \sum_{e^+ = v} f(e) = \sum_{e^- = v} f(e)
   $$
   This ensures that the total flow into any vertex (except for the source and sink) equals the total flow out, maintaining conservation of flow.

**Applications of Flow Networks**

Flow networks have numerous practical applications across various fields. Here are some notable examples:

- **Transportation and Logistics**: Modeling the movement of goods through a network of roads or shipping routes to optimize delivery times and costs.

- **Telecommunications**: Managing data transmission over networks by optimizing bandwidth usage between routers and switches.

- **Water Supply Systems**: Designing pipeline networks to efficiently distribute water from sources to consumers while considering capacity limits.

- **Electrical Grids**: Analyzing power distribution networks to ensure efficient delivery of electricity from power plants to consumers.

- **Supply Chain Management**: Optimizing resource allocation in manufacturing and distribution systems to minimize costs and maximize efficiency.

- **Network Routing**: Improving data packet routing in computer networks to enhance speed and reliability.

- **Project Scheduling**: Utilizing flow networks in project management for resource allocation and scheduling tasks based on dependencies and capacities.


## II. The Max-Flow Min-Cut Theorem

**Formal Statement of the Theorem**

The **Max-Flow Min-Cut Theorem** states that in a flow network $ (G, s, t, c) $, the maximum flow $ f^* $ from the source $ s $ to the sink $ t $ is equal to the capacity of the minimum cut separating $ s $ and $ t $$. Formally, this can be expressed as:

$$
f^* = \min_{(S, T)} c(S, T)
$$

where:
- $ f^* $ is the value of the maximum flow.
- $ (S, T) $ is an $ s-t $ cut in the graph $ G $.
- $ c(S, T) $ represents the total capacity of edges crossing from set $ S $ (containing the source) to set $ T $ (containing the sink).

**Overview of the Proof**

The proof of the Max-Flow Min-Cut Theorem can be summarized in several key steps:

1. **Establishing Upper Bound**:
   - For any flow $ f $ through a network and any cut $ (S, T) $, it holds that:
   $$
   f(G) \leq c(S, T)
   $$
   This establishes that the value of any flow cannot exceed the capacity of any cut.

2. **Existence of Maximal Flow and Minimal Cut**:
   - There exists a flow with maximum value and a cut with minimal capacity. This is derived from the properties of flows and cuts in finite networks.

3. **Constructing a Cut from a Max Flow**:
   - If there is a flow with no augmenting paths remaining (i.e., it is maximal), we can construct a cut $ (S, T) $. Set $ S $ consists of all vertices reachable from $ s $ in the residual graph, while $ T = V - S $. The capacity of this cut will equal the value of the maximum flow.

4. **Equivalence**:
   - The theorem shows that if a flow is maximal, then there exists an associated cut whose capacity equals this maximum flow. Conversely, if a cut has minimal capacity, then there exists a flow that saturates this cut.

**Importance of the Theorem**

The Max-Flow Min-Cut Theorem is crucial for several reasons:

- **Optimization Foundation**: It provides a theoretical foundation for solving various optimization problems in network design and resource allocation.

- **Duality in Linear Programming**: The theorem exemplifies duality in linear programming, linking primal problems (maximizing flow) to dual problems (minimizing cuts).

- **Algorithm Development**: It has led to efficient algorithms for computing maximum flows (e.g., Ford-Fulkerson and Edmonds-Karp), which are widely used in practice.

- **Applications Across Disciplines**: The theorem's implications extend beyond computer science into fields like operations research, telecommunications, transportation engineering, and economics, making it a versatile tool for analyzing complex systems.


## III. Ford-Fulkerson Algorithm

The **Ford-Fulkerson algorithm** is a method for computing the maximum flow in a flow network. It operates by repeatedly finding augmenting paths from the source to the sink and increasing the flow along these paths until no more augmenting paths can be found. The basic idea is to utilize the residual capacities of the edges to determine how much additional flow can be pushed through the network.

**Detailed Steps**

1. **Initialization**:
   - Start with an initial flow $ f(e) = 0 $ for all edges $ e \in E $.
   - Construct a **residual graph** $ G_f $, where each edge has a capacity equal to its original capacity minus the flow through that edge. For each edge $ (u, v) $ with capacity $ c(u, v) $, the residual graph includes:
     - The original edge with capacity $ c(u, v) - f(u, v) $
     - A reverse edge $ (v, u) $ with capacity equal to the flow that has been sent through it, i.e., $ f(u, v) $.

2. **Finding Augmenting Paths**:
   - While there exists an augmenting path from the source $ s $ to the sink $ t $ in the residual graph (using either Depth-First Search (DFS) or Breadth-First Search (BFS)), perform the following:
     - Identify the path and determine its bottleneck capacity (the minimum residual capacity along this path).
     - Augment the flow along this path by this bottleneck value.

3. **Updating Flows**:
   - For each edge in the augmenting path:
     - Increase the flow along the forward edges by the bottleneck value.
     - Decrease the flow along the reverse edges by the same amount (to account for potential future adjustments).

4. **Termination**:
   - The algorithm terminates when no more augmenting paths can be found in the residual graph.
   - The maximum flow is then given by the total flow out of the source (or equivalently into the sink).

**Code**


```python
def ford_fulkerson_(G, find_path):
    f = {}

    while True:
        G_f = make_residual(G) # ¿can this be updated in O(1)?
        p = find_path(G_f, s, t)

        if not p:
            break

        c[p] = min(c(u,v) for (u,v) in p) # bottleneck edge

        for (u,v) in p:
            f[u,v] += c(p)

    return f
```

**Complexity Analysis**

- The time complexity of the Ford-Fulkerson algorithm depends on how augmenting paths are found:
  - If DFS is used to find paths, it can lead to an exponential number of iterations in some cases, particularly when dealing with irrational capacities.
  - If BFS is used (as in Edmonds-Karp), it guarantees polynomial time complexity of $ O(VE^2) $, where $ V $ is the number of vertices and $ E $ is the number of edges.

**Key Points to Note**

- **Capacity Scaling**: The algorithm can be enhanced using a capacity scaling technique that focuses on larger capacities first, improving efficiency.
- **Integer Capacities**: If all capacities are integers, then Ford-Fulkerson will always terminate with an integer maximum flow.


## IV. Edmonds-Karp Algorithm

The **Edmonds-Karp algorithm** is a specific implementation of the Ford-Fulkerson method for computing the maximum flow in a flow network. Developed independently by Jack Edmonds and Richard Karp in 1972, this algorithm enhances the original Ford-Fulkerson approach by using **breadth-first search (BFS)** to find augmenting paths, ensuring that the paths found are the shortest in terms of the number of edges.

**Key Steps of the Algorithm**

1. **Initialization**: Start with zero flow on all edges.
2. **Finding Augmenting Paths**: Use BFS to find the shortest augmenting path from the source to the sink in the residual graph.
3. **Augment Flow**: If an augmenting path is found, determine the maximum flow that can be pushed along this path, which is equal to the minimum residual capacity of the edges in the path.
4. **Update Residual Graph**: Adjust the residual capacities of the edges along the augmenting path accordingly.
5. **Repeat**: Continue this process until no more augmenting paths can be found.

**Code**


```python
def bfs(G):
    # ...

def edmond_karp(G):
    return ford_fulkerson(G, bfs)
```

**Time Complexity**

The time complexity of the Edmonds-Karp algorithm is $ O(VE^2) $, where:
- $ V $ is the number of vertices.
- $ E $ is the number of edges.

This efficiency arises because each BFS takes $ O(E) $ time, and there can be at most $ O(VE) $ augmentations before reaching a maximum flow.


## V. Push-Relabel Algorithm


### Introduction to the Push-Relabel Algorithm

The **Push-Relabel algorithm** is a powerful method for solving the maximum flow problem in flow networks, introduced in the mid-1980s. Unlike traditional augmenting path algorithms, such as Ford-Fulkerson and Edmonds-Karp, which incrementally augment flow along paths from the source to the sink, the push-relabel approach utilizes a different strategy that focuses on managing excess flow at vertices.

**Motivation for Push-Relabel**

The motivation behind the push-relabel algorithm stems from the observation that in certain network configurations, particularly those with high-capacity edges and numerous paths, traditional algorithms can be inefficient. For instance, in a network where a large amount of flow must be routed through a single vertex before being distributed across multiple paths, it is inefficient to repeatedly explore long paths in each iteration. Instead, the push-relabel algorithm allows for the direct routing of flow to an intermediary vertex and then redistributing it across available paths.

**Key Concepts**

1. **Preflow**: The push-relabel algorithm relaxes the standard flow conservation constraints by allowing vertices (except for the source and sink) to have excess flow. This means that the total incoming flow can exceed outgoing flow, creating a "preflow" state.

2. **Excess Flow**: The excess at a vertex is defined as the difference between incoming and outgoing flow. The goal of the algorithm is to manage this excess effectively by pushing it towards the sink.

3. **Height Function**: Each vertex is assigned a height that helps determine how flow can be pushed through the network. The height indicates the potential for pushing flow downhill; edges are only traversed if they lead to vertices of lower height.

4. **Push and Relabel Operations**: The algorithm employs two main operations:
   - **Push**: Flow is pushed from a vertex with excess to an adjacent vertex if there is an admissible edge (one that allows flow based on height).
   - **Relabel**: If no pushes can be made from a vertex (i.e., all adjacent edges are flat or uphill), its height is increased to allow for future pushes.

The push-relabel algorithm maintains specific invariants throughout its execution, ensuring that it ultimately produces a valid maximum flow. By strategically managing excess flow and utilizing local adjustments rather than global augmentations, this algorithm provides an efficient solution to complex maximum flow problems, making it a preferred choice in many practical applications despite its more intricate conceptual framework compared to earlier methods.

The **Push-Relabel algorithm** employs two fundamental operations—**push** and **relabel**—to manage flow within a network. These operations are crucial for effectively redistributing excess flow and maintaining the invariants necessary for achieving maximum flow.

#### Push Operation

The **push** operation allows flow to be sent from one vertex to another, effectively transferring excess flow to adjacent vertices in the network. The operation can be described as follows:

1. **Select an Outgoing Edge**: Choose an outgoing edge $ (v, w) $ from the current vertex $ v $ in the residual graph $ G_f $. This edge must satisfy the condition that it is admissible, meaning that it can carry flow based on the current height of the vertices:
   - The height of vertex $ v $ must be exactly one greater than that of vertex $ w$: $ h(v) = h(w) + 1 $.

2. **Determine Flow to Push**: Calculate the amount of flow $ \Delta $ that can be pushed along the edge $ (v, w) $:
   $
   \Delta = \min(\alpha_f(v), \text{residual capacity of } (v, w))
   $
   Here, $ \alpha_f(v) $ represents the excess flow at vertex $ v$.

3. **Update Preflow**: Push $ \Delta $ units of flow along the edge:
   - If $ (v, w) $ is a forward edge in the original graph, increase the flow $ f(v, w) $ by $ \Delta$.
   - If it is a reverse edge $ (w, v) $, decrease the flow $ f(w, v) $ by $ \Delta$.

4. **Adjust Residual Capacities**: Update the residual capacities in the residual graph accordingly.

The push operation allows for rapid redistribution of excess flow from vertices with positive excess to their neighbors, facilitating a more efficient path towards achieving maximum flow.

#### Relabel Operation

The **relabel** operation is employed when a vertex cannot push any excess flow due to a lack of admissible edges. This operation increases the height of the vertex to potentially create new opportunities for pushing flow in subsequent iterations:

1. **Identify Need for Relabeling**: When a vertex $ v $ has positive excess but no outgoing edges that can accept flow (i.e., all outgoing edges are either flat or uphill), it is time to relabel.

2. **Increase Height**: Increase the height of vertex $ v $:
   $$
   h(v) = h(v) + 1
   $$

3. **Maintain Invariants**: The relabel operation ensures that the height invariants are maintained:
   - The new height allows for potential pushes along edges that may have become admissible as a result of this change.

By systematically applying push and relabel operations, the algorithm works towards eliminating excess flows at each vertex while maintaining critical invariants that guarantee convergence to a maximum flow solution. This dual operation strategy allows for effective management of flows within complex networks and enhances overall computational efficiency.

### Analysis

The analysis of the Push-Relabel algorithm involves quantifying the number of operations performed during its execution, specifically focusing on the bounds of relabels and pushes. The following formalization summarizes these key points:

1. **Bounding Relabels**:
   - Each vertex in the network can only be relabeled a maximum of $ O(n) $ times. This is due to the fact that the height of each vertex can increase until it reaches a maximum height of $ n $, where $ n $ is the number of vertices in the graph.
   - Consequently, for a network with $ n $ vertices, the total number of relabel operations across all vertices is bounded by:
     $
     O(n^2)
     $

2. **Bounding Saturating Pushes**:
   - Each edge in the network can experience at most $ O(n) $ saturating pushes. This is because an edge can only be saturated once for each pair of relabels applied to both its endpoints.
   - Therefore, if there are $ m $ edges in the graph, the total number of saturating pushes is bounded by:
     $
     O(mn)
     $

3. **Bounding Non-Saturating Pushes**:
   - Each vertex can undergo at most $ O(n^2) $ non-saturating pushes. This is because there can only be one non-saturating push per phase for each vertex.
   - Given that there are $ n $ vertices, the total number of non-saturating pushes across all vertices is bounded by:
     $
     O(n^3)
     $

The overall performance analysis leads to the following conclusions regarding the bounds on operations in the Push-Relabel algorithm:

- **Total Relabels**:
  $
  O(n^2)
  $

- **Total Saturating Pushes**:
  $
  O(mn)
  $

- **Total Non-Saturating Pushes**:
  $
  O(n^3)
  $

**However** in practice, they often work in $O(n^2)$ or faster !!
