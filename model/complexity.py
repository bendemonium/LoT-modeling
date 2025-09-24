from contextvars import ContextVar
from collections import defaultdict
from dataclasses import dataclass
from contextlib import contextmanager
import threading
from typing import Optional, Dict, Any
from functools import wraps
from collections import deque

_CURRENT_RUN: ContextVar[Optional["RunScope"]] = ContextVar("_CURRENT_RUN", default=None)

class Space:
    def __init__(self):
        self.active: Dict[int, float] = {}
        self.total = 0.0
        self.max_seen = 0.0
        self.lock = threading.Lock()

    def register(self, obj: Any, weight: float):
        oid = id(obj)
        with self.lock:
            if oid not in self.active:
                self.active[oid] = weight
                self.total += weight
                self.max_seen = max(self.max_seen, self.total)

    def update(self, obj: Any, weight: float):
        oid = id(obj)
        with self.lock:
            old = self.active.get(oid, 0.0)
            self.active[oid] = weight
            self.total += weight - old
            self.max_seen = max(self.max_seen, self.total)

    def purge(self, obj: Any):
        oid = id(obj)
        with self.lock:
            w = self.active.pop(oid, 0.0)
            self.total -= w

class Kolmo:
    def __init__(self):
        self.counts = defaultdict(int)
        self.total = 0.0

    def record(self, pf_name: str, weight: float):
        self.counts[pf_name] += 1
        self.total += float(weight)

class RunScope:
    def __init__(self):
        self.space = Space()
        self.kolmo = Kolmo()

@dataclass
class RunSnapshot:
    mdl: int
    k_complexity_breakdown: Dict[str, int]
    space_complexity: float

class Complexity:
    def __init__(self):
        self.runs: list[RunSnapshot] = []
        self.end: Optional[RunSnapshot] = None

    @contextmanager
    def activate(self):
        parent = _CURRENT_RUN.get()
        scope = RunScope()
        token = _CURRENT_RUN.set(scope)
        try:
            yield
        finally:
            _CURRENT_RUN.reset(token)
            if parent is not None:
                _CURRENT_RUN.set(parent)
            snap = RunSnapshot(
                mdl=scope.kolmo.total,
                k_complexity_breakdown=dict(scope.kolmo.counts),
                space_complexity=scope.space.max_seen,
            )
            self.runs.append(snap)
            self.last = snap

    def purge(self):
        self.runs.clear()
        self.last = None

    @property
    def cf_mdl(self) -> float:
        return sum(r.mdl for r in self.runs)

    @property
    def cf_space(self) -> float:
        return max((r.space_complexity for r in self.runs), default=0.0)

from functools import wraps
from collections import deque
from typing import Any

def _is_mem_obj(x: Any) -> bool:
    # Duck-type check for your memory-tracked objects
    return hasattr(x, "compute_weight") and callable(x.compute_weight) and getattr(x, "_track", True)

def cognitive_function():
    """
    Wrap a run function to:
      - Create a fresh Complexity/RunScope
      - Auto-register top-level Mem objects in args/kwargs
      - Return (result, complexity)
    """
    def deco(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            comp = Complexity()
            with comp.activate():
                scope = _CURRENT_RUN.get()
                if scope is not None:
                    seen = set()
                    # Top-level scan of args
                    for a in args:
                        if _is_mem_obj(a) and id(a) not in seen:
                            seen.add(id(a))
                            scope.space.register(a, a.compute_weight())
                    # Top-level scan of kwargs
                    for a in kwargs.values():
                        if _is_mem_obj(a) and id(a) not in seen:
                            seen.add(id(a))
                            scope.space.register(a, a.compute_weight())
                result = fn(*args, **kwargs)
            return result, comp
        return wrapped
    return deco