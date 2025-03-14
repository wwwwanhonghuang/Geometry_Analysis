from data_structures.grammar.geometric_graph_grammar import GeometricGraphGrammar
from data_structures.geometric_graph import GeometricGraph
from typing import List
import numpy as np
class GraphAnalyzerContext():
    def __init__(self, geometric_graph: GeometricGraph):
        self.geometric_graph :GeometricGraph = geometric_graph
        self.isogroups : ISOGroups = ISOGroups()
        self.storage = {}

    def set(self, key: str, value: any):
        self.storage[key] = value
    
    def get(self, key: str):
        if not key in self.storage:
            return None
        return self.storage[key]


class ISOGroup:
    def __init__(self):
        self.graphs : List[GeometricGraph] = []

    def size(self):
        return len(self.graphs)
    
    def add_graph(self, graph: GeometricGraph):
        self.graphs.append(graph)

    def get_graphs(self):
        return self.graphs

    def __str__(self):
        return f"(size: {self.size()}, value: {str(self.graphs)})"
     
    def __repr__(self):
        return self.__str__()
    
class ISOGroups:
    def __init__(self):
        self.isogroups : List[ISOGroup] = []

    def add_graph_to_isogroup(self, graph):
        """Add a graph to the appropriate isogroup, or create a new isogroup if none match."""
        for group in self.isogroups:
            if any(is_isomorphic(graph, existing_graph) for existing_graph in group.get_graphs()):
                group.add_graph(graph)
                return
        
        # If no matching isogroup was found, create a new one
        new_group = ISOGroup()
        new_group.add_graph(graph)
        self.isogroups.append(new_group)

    def is_isomorphic(graph1: GeometricGraph, graph2: GeometricGraph):
        """Placeholder function for graph isomorphism checking."""
        # Implement actual isomorphism checking logic here
        if graph1.dim != graph2.dim or len(graph1.V) != len(graph2.V) or len(graph1.E) != len(graph2.E):
            return False
        
        # Normalize vertex order by sorting V
        V1_sorted_idx = np.lexsort(graph1.V.T)
        V2_sorted_idx = np.lexsort(graph2.V.T)

        V1_sorted = graph1.V[V1_sorted_idx]
        V2_sorted = graph2.V[V2_sorted_idx]

        # Normalize edges based on sorted vertex order
        index_map = {old_idx: new_idx for new_idx, old_idx in enumerate(V1_sorted_idx)}
    
        E1_normalized = sorted([sorted([index_map[e[0]], index_map[e[1]]]) for e in graph1.E])
        E2_normalized = sorted([sorted(e) for e in graph2.E])


        return np.array_equal(V1_sorted, V2_sorted) and E1_normalized == E2_normalized

    def size(self):
        return len(self.isogroups)
    
    def add_group(self, group):
        """Add an isomorphism group."""
        self.isogroups.append(group)

    def get_groups(self):
        """Return the list of isomorphism groups."""
        return self.isogroups
    
    def __str__(self):
        return str(self.isogroups)
 
    def __repr__(self):
        return self.__str__()
    

class GraphAnalyzer():
    def __init__(self):
        pass
    
    def _extend_more(self, ctx: GraphAnalyzerContext):
        

        isogroup_detection_stop_strategy = ctx.get("isogroup_detection_stop_strategy")
        last_n_isogroups = ctx.get("last_n_isogroups")

        if last_n_isogroups == ctx.isogroups.size():
            return False
        
        if isogroup_detection_stop_strategy is not None and isogroup_detection_stop_strategy(ctx):
            return False

        return True


    def normalize_graphs(self, graphs):
        from scipy.spatial.transform import Rotation as R

        # 1. Normalize all graphs based on their centroid.
        # 2. Apply scaling (optional, based on your needs).
        # 3. Apply rotation (e.g., aligning them based on their first vertex or orientation).
        
        for graph in graphs:
            # Step 1: Compute centroid
            centroid = np.mean(graph.V, axis=0)
            
            # Step 2: Translate the graph to the origin (centroid alignment)
            graph.V -= centroid
            
            # Step 3: Scale the graph (optional, can be based on a reference distance or a fixed scale)
            scale_factor = np.linalg.norm(graph.V)  # You can adjust this as needed
            graph.V /= scale_factor
            
            # Step 4: Align graphs via rotation (if necessary, to match orientation)
            # Let's rotate around the first vertex to a common reference axis (for example, align to x-axis).
            first_vertex = graph.V[0]
            rotation_angle = np.arctan2(first_vertex[1], first_vertex[0])
            rotation_matrix = R.from_euler('z', -rotation_angle).as_matrix()  # Rotate in the 2D plane
            
            # Apply rotation to all vertices
            graph.V = graph.V.dot(rotation_matrix.T)

        return graphs

    def _vertex_expansion(self, ctx: GraphAnalyzerContext):

        graph = ctx.geometric_graph
        groups = ctx.isogroups
        
        next_order_groups = ISOGroups()

        
        extended_graphs = []

        for group in groups.get_groups():
            for graph in group.get_graphs():
                # We have normalized the graph that, the first vertex in the graph is 
                # alway the point to extend from
                extend_vertex = graph.V[0, :]

                # Iterate edges that connect to the vertex we aim to extend
                for edge in filter(lambda e: np.array_equal(graph.V[e[0], :], extend_vertex) or np.array_equal(graph.V[e[1], :], extend_vertex), graph.E):
                    if [0, edge[0]] not in graph.E and [0, edge[1]] not in graph.E and \
                        [edge[0], 0] not in graph.E and [edge[1], 0] not in graph.E:
                        new_graph : GeometricGraph = graph.copy()
                        new_graph.E.append(edge)
                        
                       
                        extended_graphs.append(new_graph)
        
        '''
            Normalization is done such
            that all expanded graphs are aligned to each other (same scale and rotation).
        '''
        extended_graphs = self.normalize_graphs(extended_graphs)
        for extended_graph in extended_graphs:
            next_order_groups.add_graph_to_isogroup(extended_graph)
        ctx.isogroups = next_order_groups
        return next_order_groups

    def _isogroups_filtering(self, ctx: GraphAnalyzerContext):
        isogroups_filtering_strategy = ctx.get("isogroup_filtering_strategy")
        if isogroups_filtering_strategy is not None:
            ctx.isogroups = isogroups_filtering_strategy(ctx.isogroups)
            return ctx.isogroups
        return ctx.isogroups

    def _isogroup_detection(self, ctx: GraphAnalyzerContext):
        while True:
            if not self._extend_more(ctx):
                break

            self._vertex_expansion(ctx)
            self._isogroups_filtering(ctx)

    def _isogroup_selection(self, ctx: GraphAnalyzerContext):
        isogroups_filtering_strategy = ctx.get("isogroup_filtering_strategy")
        if isogroups_filtering_strategy is not None:
            ctx.isogroups = isogroups_filtering_strategy(ctx.isogroups)
            return ctx.isogroups
        return ctx.isogroups


    def _more_isogroups(self, ctx: GraphAnalyzerContext):
        """
        Determine whether to extend the search for more isomorphism groups.
        """
        last_n_isogroups = ctx.get("last_n_isogroups")
        if last_n_isogroups == ctx.isogroups.size():
            return False
        
        stop_strategy = ctx.get("isogroups_generation_stop_strategy")
        if stop_strategy is not None and stop_strategy(ctx):
            return False
        
        return True

    def _generate_initial_isogroups(self, ctx: GraphAnalyzerContext):
        graph : GeometricGraph = ctx.geometric_graph
        # each single edges as an isogroup
        isogroup = ISOGroup()
        for edge in graph.E:
            vertex_1 = edge[0]
            vertex_2 = edge[1]
            single_edge_graph = GeometricGraph(graph.V[[vertex_1, vertex_2], :], [[vertex_1, vertex_2]], graph.dim)
            isogroup.add_graph(single_edge_graph)
        ctx.isogroups.add_group(isogroup)

    def analyze(self, geometric_graph: GeometricGraph):
        ctx = GraphAnalyzerContext(geometric_graph)
        
        ctx.set("last_n_isogroups", -1)

        self._generate_initial_isogroups(ctx)

        while True:
            if not self._more_isogroups(ctx):
                break
            ctx.set("last_n_isogroups", ctx.isogroups.size())
            self._isogroup_detection(ctx)
            self._isogroup_selection(ctx)

        
        return ctx.isogroups

        
class GraphGrammarEncoder:
    def __init__(self):
        raise NotImplementedError