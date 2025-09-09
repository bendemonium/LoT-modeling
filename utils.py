from functools import cached_property, cache, partial
import time
from operator import attrgetter
from tabulate import tabulate
import networkx as nx
from typing import Literal
import matplotlib.pyplot as plt
from dataclasses import dataclass
import primitive_fucntions as pf

# ---------------------------------------------------------------------#

class Element: # n-dimensional element
    def __init__(self, name, attribute1, attribute2=None):
        self.name = name
        self.attribute1 = attribute1
        self.attribute2 = attribute2
    def __repr__(self): 
        return f"Element(object={self.name}, attribute 1={self.attribute1}, attribute 2={self.attribute2})"
    def __str__(self):
        return f"{self.name}, {self.attribute1}, {self.attribute2})"

@dataclass
class  Associations: # n-dimensional association
    associations: dict
    positional: bool = False
    def __repr__(self):
        raise NotImplementedError
    def build_updates(self, graph):
        if self.positional:
            for key, value in self.associations.items():
                nx.set_node_attributes(graph, {key.name: {"position": value}})
        else:
            for key, value in self.associations.items():
                graph.add_edge(key.name, value.name, label="precedes", directed=True)


'''
class ElementSet: # n-dimensional element set
    def __init__(self, elements: set, associations: Associations = None):
        self.elements = elements
        self.associations = associations
        self.graph = self.build_graph()
    def __repr__(self):
        raise NotImplementedError
    def build_graph(self):
        G = nx.MultiGraph()  # Create a directed graph
        for obj in self.elements:
            G.add_node(obj.name, type='element')  # Add object as a node
            G.add_node(obj.attribute1, type='attribute1')  # Add color as a node
            G.add_edge(obj.name, obj.attribute1, label="attribute")  # Add directed edge with label
            if obj.attribute2:
                # If the object has a second attribute, add it as a node and edge
                G.add_node(obj.attribute2, type='attribute2')  # Add shape as a node
                G.add_edge(obj.name, obj.attribute2, label="attribute")
        if  self.associations:
            self.associations.build_updates(G)  # Build associations
        if self.graph:
            self.graph = G
        return G
    def visualize(self):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)

        # Draw nodes with different colors based on type
        node_colors = []
        for node, data in self.graph.nodes(data=True):
            if data['type'] == 'element':
                node_colors.append('skyblue')
            elif data['type'] == 'attribute1':
                node_colors.append('lightgreen')
            elif data['type'] == 'attribute2':
                node_colors.append('lightcoral')

        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10)
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()
    @cached_property
    def attribute1_types(self):
        """Returns a set of unique attribute1 types."""
        return set(obj.attribute1 for obj in self.elements)
    @cached_property
    def attribute2_types(self):
        """Returns a set of unique attribute2 types."""
        return set(obj.attribute2 for obj in self.elements if obj.attribute2 is not None)
    def attribute_items(self, attribute):
        def get_type(type_):
            
            return getattr(self, f"{attribute}_types", set())



'''


def pretty_view(sequence):
    """Prints a sequence of elements in a pretty format."""
    cute = list(zip(*map(attrgetter("name", "attribute1", "attribute2"), sequence)))
    # Print as a table
    print(tabulate(zip(*cute), headers=["object", "attribute 1", "attribute 2"], tablefmt="grid"))



# ---------------------------------------------------------------------#

class Stopwatch:
    def __init__(self):
        self._start_time = None
        self._elapsed_time = 0
        self._running = False
        
    def start(self):
        """Start or resume the stopwatch."""
        if not self._running:
            self._start_time = time.perf_counter() - self._elapsed_time
            self._running = True
            # print("Stopwatch started.")

    def stop(self):
        """Stop the stopwatch and display the elapsed time."""
        if self._running:
            self._elapsed_time = time.perf_counter() - self._start_time
            self._running = False
            # print(f"Stopwatch stopped. Elapsed time: {self._elapsed_time:.2f} seconds.")

    def reset(self):
        """Reset the stopwatch to zero."""
        self._elapsed_time = 0
        if self._running:
            self._start_time = time.perf_counter()
        # print("Stopwatch reset.")

    def get_elapsed_time(self):
        """Get the current elapsed time without stopping the stopwatch."""
        if self._running:
            return time.perf_counter() - self._start_time
        return self._elapsed_time

class SpaceComplexity:
    """
    Tracks space complexity for temporary variables in cognitive functions.
    Use startcounttemp(x) to add x units, subtemp(x) to subtract x units.
    get_max() returns the maximum count reached.
    """
    def __init__(self):
        self.count = 0
        self.max = 0
    def startcounttemp(self):
        self.count += 1
        if self.count > self.max:
            self.max = self.count
    def subtemp(self):
        self.count -= 1
    def get_max(self):
        return self.max
    def reset(self):
        self.count = 0
        self.max = 0

class ElementSet: # n-dimensional element set
    def __init__(self, elements: set, associations: Associations = None):
        self.elements = elements
        self.associations = associations
    def __repr__(self):
        raise NotImplementedError
    def attribute1_types(self):
        """Returns a set of unique attribute1 types."""
        return set(obj.attribute1 for obj in self.elements)
    def attribute2_types(self):
        """Returns a set of unique attribute2 types."""
        return set(obj.attribute2 for obj in self.elements if obj.attribute2 is not None)
    def attribute_items(self, attribute):
        def get_type(type_):
            
            return getattr(self, f"{attribute}_types", set())
