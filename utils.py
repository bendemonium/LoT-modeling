from functools import cached_property, cache, partial
import time
from operator import attrgetter
from tabulate import tabulate
import networkx as nx
from typing import Literal
import matplotlib.pyplot as plt
from dataclasses import dataclass
import primitive_fucntions as pf
import importlib
import copy
from collections import defaultdict
import numpy as np

# ---------------------------------------------------------------------#

"""
@dataclass
class Element: # n-dimensional element
    name : str
    attribute1 : int | float | str
    attribute2 : int | float | str | None = None
    def __repr__(self): 
        return f"Element(object={self.name}, attribute 1={self.attribute1}, attribute 2={self.attribute2})"
    def __str__(self):
        return f"{self.name}, {self.attribute1}, {self.attribute2})"
"""

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
            if hasattr(self, 'graph') and self.graph:
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

class KComplexity:
    def __init__(self):
        self.prim = importlib.import_module('primitive_fucntions')
        self.cog = importlib.import_module('cognitive_functions')
        self.call_counts = {}
        self.total_calls = {}
        self.cog_func_calls = defaultdict(list)
        self._wrap_prim_functions()
        self._wrap_cog_functions()
        self.current_cog_name = None

    def _wrap_prim_functions(self):
        for name in dir(self.prim):
            func = getattr(self.prim, name)
            if callable(func) and not name.startswith("__"):
                self.call_counts[name] = 0
                self.total_calls[name] = 0
                wrapper_func = self._make_prim_wrapper(func, name)
                setattr(self.prim, name, self._make_prim_wrapper(func, name))

    def _wrap_cog_functions(self):
        for name in dir(self.cog):
            if name.startswith("__") or name == "find_bias":
                continue
            func = getattr(self.cog, name)
            if callable(func):
                setattr(self.cog, name, self._make_cog_wrapper(func, name))

    def _make_prim_wrapper(self, func, name):
        def wrapper(*args, **kwargs):
            self.call_counts[name] += 1
            self.total_calls[name] += 1
            return func(*args, **kwargs)
        return wrapper

    def _make_cog_wrapper(self, func, name):
        def wrapper(*args, **kwargs):
            self.reset() 
            result = func(*args, **kwargs)
            self.cog_func_calls[name].append(copy.deepcopy(self.call_counts))
            self.current_cog_name = name
            return result
        return wrapper
    
    def get_cog_name(self):
        return self.current_cog_name

    def get_prim_counts(self):
        return dict(self.call_counts)
    
    def get_total_prim_counts(self):
        return dict(self.total_calls)

    def get_k_complexity(self):
        return sum(self.call_counts.values())
    
    def get_total_k_complexity(self):
        return sum(self.total_calls.values())

    def reset(self):
        for key in self.call_counts:
            self.call_counts[key] = 0

    def plot_prim_counts(self):
        data = self.get_prim_counts()
        plt.bar(data.keys(), data.values())
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Call Count")
        plt.title(self.get_cog_name() + " Primitive Function Usage")
        plt.tight_layout()
        plt.show()

    def plot_total_prim_counts(self):
        data = self.get_total_prim_counts()
        plt.bar(data.keys(), data.values())
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Call Count")
        plt.title("Total Primitive Function Usage")
        plt.tight_layout()
        plt.show()

    def plot_cog_vs_prim(self):
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        import matplotlib.colors as mcolors

        prim_names = list(self.call_counts.keys())

        valid_cog_fns = {"iterate", "palindrome", "alternate", "chaining", "seriate", "serial_crossed", "center_embedded", "tail_recursive"}
        cog_names = [cog for cog in self.cog_func_calls if cog in valid_cog_fns and len(self.cog_func_calls[cog]) > 0]

        averaged_data = []
        cog_labels = []
        for cog in cog_names:
            call_count = len(self.cog_func_calls[cog])
            cog_labels.append(f"{cog} ({call_count}x)")

            summed = defaultdict(int)
            for d in self.cog_func_calls[cog]:
                for k in d:
                    summed[k] += d[k]
            avg = {k: summed[k] / call_count for k in prim_names}
            averaged_data.append(avg)

        color_map = cm.get_cmap('tab20', len(prim_names))
        colors = {prim: color_map(i) for i, prim in enumerate(prim_names)}

        bottom = np.zeros(len(cog_labels))
        for prim in prim_names:
            heights = [d[prim] for d in averaged_data]
            plt.bar(cog_labels, heights, bottom=bottom, label=prim, color=colors[prim])
            bottom += heights

        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Total Primitive Calls")
        plt.title("All Cognitive Function Calls with Primitive Usage Breakdown")
        plt.legend(title="Primitive Functions", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
