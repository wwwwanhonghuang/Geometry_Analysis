from data_structures.grammar.geometric_graph_grammar import GeometricGraphGrammar
from data_structures.geometric_graph import GeometricGraph
from typing import List

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

    def __str__(self):
        return f"(size: {self.size()}, value: {str(self.graphs)})"
     
    def __repr__(self):
        return self.__str__()
class ISOGroups:
    def __init__(self):
        self.isogroups : List[ISOGroup] = []

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

    def _vertex_expansion(self, ctx: GraphAnalyzerContext):
        pass

    def _isogroups_filtering(self, ctx: GraphAnalyzerContext):
        pass

    def _isogroup_detection(self, ctx: GraphAnalyzerContext):

        while True:
            if not self._extend_more(ctx):
                break

            self._vertex_expansion()
            self._isogroups_filtering()


            
        
    def _isogroup_selection(self, ctx: GraphAnalyzerContext):
        pass

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
        print(isogroup)
        raise NotImplementedError

    def analyze(self, geometric_graph: GeometricGraph):
        ctx = GraphAnalyzerContext(geometric_graph)
        
        ctx.set("last_n_isogroups", -1)

        self._generate_initial_isogroups(ctx)

        while True:
            if not self._more_isogroups(ctx):
                break
            self._isogroup_detection(ctx)
            self._isogroup_selection(ctx)
        
        return ctx.isogroups

        
class GraphGrammarEncoder:
    def __init__(self):
        pass