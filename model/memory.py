
from contextvars import ContextVar
import weakref
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable, Set, List, Dict, Union
import networkx as nx
from copy import deepcopy

_CURRENT_RUN: ContextVar = ContextVar("_CURRENT_RUN", default=None)

class MemoryStructure:
    """
    Base class for memory-tracked objects.
    Set track=False to opt out of automatic Space bookkeeping.
    """
    __slots__ = ("_finalizer", "_track")

    def __init__(self, *, track: bool = True):
        self._track = bool(track)

        if self._track:
            scope = _CURRENT_RUN.get()
            if scope is not None:
                scope.space.register(self, self.compute_weight())
            # Only finalize/purge if we're tracking
            self._finalizer = weakref.finalize(self, MemoryStructure._on_finalize, weakref.ref(self))
        else:
            self._finalizer = None
    
    def __deepcopy__(self, memo):
        # Create a new instance
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj

        # Copy over all attributes
        if hasattr(self, "__slots__"):
            for slot in self.__slots__:
                if hasattr(self, slot):
                    setattr(new_obj, slot, copy.deepcopy(getattr(self, slot), memo))
        else:
            for k, v in self.__dict__.items():
                setattr(new_obj, k, copy.deepcopy(v, memo))

        # Re-register the new object if tracking is enabled
        if getattr(self, "_track", True):
            scope = _CURRENT_RUN.get()
            if scope is not None:
                scope.space.register(new_obj, new_obj.compute_weight())

        return new_obj

    @staticmethod
    def _on_finalize(self_ref):
        obj = self_ref()
        if obj is None or not getattr(obj, "_track", False):
            return
        scope = _CURRENT_RUN.get()
        if scope is not None:
            scope.space.purge(obj)

    def compute_weight(self) -> float:
        """Override in subclasses to return current weight."""
        return 0.0

    def _changed(self):
        """Call after updating internal state so Space can refresh weight."""
        if not self._track:
            return
        scope = _CURRENT_RUN.get()
        if scope is not None:
            scope.space.update(self, self.compute_weight())

    def purge(self):
        """Manually remove this object from tracking."""
        if not self._track:
            return
        scope = _CURRENT_RUN.get()
        if scope is not None:
            scope.space.purge(self)

class Token(MemoryStructure):
    """
    A token that can participate in a lexicon.
    """
    __slots__ = (
        "name", "attribute1", "attribute2",
        "predecessors", "successors", "ordinate"
    )

    def __init__(
        self,
        name = None,
        attribute1 = None,
        attribute2 = None,
        *,
        predecessors = None,
        successors = None,
        ordinate = None,
        **kwargs
    ):
        self.name = name
        self.attribute1 = attribute1
        self.attribute2 = attribute2
        self.predecessors: Set[Token] = set(predecessors or [])
        self.successors: Set[Token] = set(successors or [])
        self.ordinate = float(ordinate) if ordinate is not None else None
        if self.predecessors or self.succesors:
            self.linked = True
        super().__init__()(**kwargs)

    def __repr__(self):
        return f"Token({self.name!r}, linked={self.linked}, ord={self.ordinate})"

    def __bool__(self):
        return True if seld.tokens else False

    def compute_weight(self):
        weight_params = [self.attribute1, self.attribute2, self.predecessors, self.successors, self.ordinate]
        weight =  sum(1 for v in weight_params if v is not None)
        
    
class Lexicon(MemoryStructure):
    __slots__ = ("tokens", "_G", "dimension", "linked")

    def __init__(self, tokens = None, *, 
                linked = False, ordered = False, **kwargs):
        self.tokens: Set[Token] = set(tokens or [])
        self.linked = linked
        self.ordered = ordered
        self.G: nx.DiGraph = self._build_graph()
        self.ordinates = 
        super().__init__(**kwargs)
    
    def __iter__(self):
        return self.tokens

    def compute_weight(self) -> float:
        return float(len(self.tokens) + self._G.number_of_edges())

    ## maybe build a bool dunder function

    def _token_vet(token):
            G.add_node(token.name, type='token')  
            if t.attribute1:
                G.add_node(token.attribute1, type='attribute1') 
                G.add_edge(token.name, token.attribute1)  
            if t.attribute2:
                G.add_node(token.attribute2, type='attribute2') 
                G.add_edge(token.name, token.attribute2)
            if t.ordinate:
                G.add_node(token.ordinate, type='ordinate') 
                G.add_edge(token.ordinate, token.name)

    def _build_graph(self) -> nx.DiGraph:
        G = nx.MultiDiGraph()
        for t in self.tokens:
            _token_vet(t)
        if linked:
            for t in self.tokens:
                if predecessors:
                    for p in predecessors:
                        G.add_edge(p.name, t.name, label = "linked")
                if successors:
                    for s in successors:
                        G.add_edge(t.name, s.name, label = "linked")
        if ordered:
            ordinates = [n for n, data in G.nodes(data=True) if data.get("type") == "ordinate"]
            ordinates = sorted(ordinates)
            for u, v in zip(sorted_nodes, sorted_nodes[1:]):
                G.add_edge(u, v)
        return G

    @property
    def G(self) -> nx.DiGraph:
        """Access the materialized lexicon."""
        return self._G

    def add_token(self, new_token):
        added = False
        if t not in self.tokens:
            self.tokens.add(t)
            added = True
        if added:
            self._G = self._build_graph()
            self._changed()

    def remove_token(self, drop_token):
        removed = False
        if t in self.tokens:
            self.tokens.remove(t)
            removed = True
        if removed:
            self._G = self._build_graph()
            self._changed()
    
    def get_token(self, token):
        token = next((t for t in lexicon.tokens if t.name == token), None)
        if token:
            return token
        else:
            return None


    def successors(self, token: Token) -> List[Token]:
        if token not in self.tokens:
            return []
        out = []
        for n in self._G.successors(token.name):
            data = self._G.nodes[n]
            if data.get("type") == "token":
                out.append(data["token"])
        return out

    def predecessors(self, token: Token) -> List[Token]:
        if token not in self.tokens:
            return []
        out = []
        for n in self._G.predecessors(token.name):
            data = self._G.nodes[n]
            if data.get("type") == "token":
                out.append(data["token"])
        return out
    
    if ordered:
        @property
        def first(self):
            ordinates = [
                data["value"] for n, data in lexicon.G.nodes(data=True)
                if data.get("type") == "ordinate"
            ]
            lowest = min(ordinates, default=None)
            return lowest

    @classmethod
    def from_nx(cls, G: nx.DiGraph, *, track: bool = True) -> "Lexicon":
        """Reconstruct a Lexicon (and fresh Tokens) from a NetworkX subgraph."""
        # 1) Build Token objects for every token node
        tokens_by_name: dict[str, Token] = {}
        for n, data in G.nodes(data=True):
            if data.get("type") == "token":
                t = Token(
                    name=n,
                    attribute1=data.get("attribute1"),
                    attribute2=data.get("attribute2"),
                    predecessors=[],   # filled next
                    successors=[],     # filled next
                    ordinate=None,     # filled next (if any)
                    track=False,       # delay tracking to Lexicon instance
                )
                tokens_by_name[n] = t

        # 2) Wire token→token edges (successors/predecessors)
        for u, v, ed in G.edges(data=True):
            if ed.get("label") == "token_edge":
                tu = tokens_by_name.get(u)
                tv = tokens_by_name.get(v)
                if tu is not None and tv is not None:
                    tu.successors.append(tv)
                    tv.predecessors.append(tu)

        # 3) Attach ordinates from token -> ("ord", value) edges
        for u, v, ed in G.edges(data=True):
            if ed.get("label") == "has_ordinate":
                tok = tokens_by_name.get(u)
                if tok is not None:
                    # v should be ("ord", value)
                    if isinstance(v, tuple) and len(v) == 2 and v[0] == "ord":
                        tok.ordinate = float(v[1])

        # 4) Construct the Lexicon. Its __init__ will auto-register (track flag here).
        #    Pass tokens as an iterable; Lexicon will build its internal graph.
        new_lex = cls(tokens=tokens_by_name.values(), track=track)
        return new_lex

    @classmethod
    def from_subgraph_nodes(cls, G: nx.DiGraph, nodes, *, track: bool = True) -> "Lexicon":
        """Convenience: take a node list from a larger graph and build a Lexicon."""
        sub = G.subgraph(nodes).copy()
        return cls.from_nx(sub, track=track)

class List(MemoryStructure):
    """Memory object representing a list; weight = list length."""
    __slots__ = ("items",)

    def __init__(self, items=None, **kwargs):
        self.items = deque(items) if items is not None else []
        super().__init__(**kwargs)

    def compute_weight(self) -> float:
        return int(len(self.items))

    def suffix(self, value):
        self.items.append(value)
        self._changed()

    def prefix(self, values):
        self.items.appendleft(values)
        self._changed()

    def clear(self):
        self.items.clear()
        self._changed()

    def reverse(self):
        self.items = deque(reversed(self.items))
        self._changed()
    
    def clone(self, other):
        self.items = deque(copy.deepcopy(list(other.items)))
        self._changed()

class Queue(MemoryStructure):
    """Memory object representing a queue; weight = queue length."""
    __slots__ = ("items",)

    def __init__(self, items=None, **kwargs):
        self.items = deque(items) if items is not None else []
        super().__init__(**kwargs)

    def compute_weight(self) -> float:
        return int(len(self.items))

    def push_in(self, value):
        self.items.appendleft(value)
        self._changed()

    def push_out(self):
        out = self.items.pop()
        self._changed()
        return out

    def clear(self):
        self.items.clear()
        self._changed()
    
    def clone(self, other):
        self.items = deque(copy.deepcopy(list(other.items)))
        self._changed()

class Mode(MemoryStructure):
        __slots__ = ("item",)
    def __init__(self, item=None, **kwargs):
        self.item = item
        super().__init__(**kwargs)

    def compute_weight(self) -> float:
        return 1


class Sequence:
    """The final sequence, not tracked in Space"""
    __slots__ = ("items",)

    def __init__(self, items=None):
        self.items = deque(items) if items is not None else []

    def click(self, value):
        self.items.append(value)

class Pointer(MemoryStructure):
    """The final sequence, not tracked in Space"""
    __slots__ = ("node")

    def __init__(self, items=None):
        self.items = deque(items) if items is not None else []

    def click(self, value):
        self.items.append(value)