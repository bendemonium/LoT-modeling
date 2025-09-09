import random
from utils import SpaceComplexity as sc

SEED = 42
random.seed(SEED)

# Functions on lists (strings)

# if the boolean return_space is True, the function returns a tuple (result, space_used)
# otherwise it returns just the result (as before)

def pair(L, C, return_space: bool = False):
    """Concatenate item C onto list L (in-place)."""
    sc_obj = sc()
    # pairing mutates L in-place (persistent)
    sc_obj.startcounttemp()  # account for the persistent container L
    L.append(C)
    # we keep the persistent allocation counted; no subtemp
    space_used = sc_obj.get_max()
    if return_space:
        return (None, space_used)
    return None

def append(X, Y, return_space: bool = False):
    """Append lists X and Y (returns a new list)."""
    sc_obj = sc()
    # allocating result list
    sc_obj.startcounttemp()
    result = X + Y
    space_used = sc_obj.get_max()
    if return_space:
        return (result, space_used)
    return result

# Random functions

def flip(p, return_space: bool = False):
    """Returns True with probability p."""
    sc_obj = sc()
    # trivial constant-space operation; count one slot to be explicit
    sc_obj.startcounttemp()
    val = random.random() < p
    sc_obj.subtemp()
    space_used = sc_obj.get_max()
    if return_space:
        return (val, space_used)
    return val

# Set functions

def setminus(set1, s, return_space: bool = False):
    """Remove an item from a set in-place."""
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent container set1 counted
    set1.remove(s)
    space_used = sc_obj.get_max()
    if return_space:
        return (None, space_used)
    return None

def sample(collection, return_space: bool = False):
    """
    Sample one element from set or list.
    Returns element (or None if empty). Default behavior unchanged.
    """
    sc_obj = sc()
    sc_obj.startcounttemp()  # sampling overhead
    if not collection:
        sc_obj.subtemp()
        space_used = sc_obj.get_max()
        if return_space:
            return (None, space_used)
        return None

    if isinstance(collection, set):
        # convert to tuple for sampling (temporary)
        sc_obj.startcounttemp()
        collection = tuple(collection)
        sc_obj.subtemp()

    val = random.sample(collection, 1)[0]
    sc_obj.subtemp()
    space_used = sc_obj.get_max()
    if return_space:
        return (val, space_used)
    return val

# Token-related / utility functions

def add(T, lst, return_space: bool = False):
    """Return a new list with T appended (tracks space)."""
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent result
    result = lst.copy()
    result.append(T)
    space_used = sc_obj.get_max()
    if return_space:
        return (result, space_used)
    return result

def remove(T, lst, return_space: bool = False):
    """Return a copy of list with T removed (tracks space)."""
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent result
    result = lst.copy()
    if T in result:
        result.remove(T)
    space_used = sc_obj.get_max()
    if return_space:
        return (result, space_used)
    return result

def write_random(G, bias, type, return_space: bool = False):
    """
    Given a NetworkX graph G, find nodes 'u' such that there is an edge (u -> v)
    with v == type and edge data label == bias. Return a randomly-selected u or None.
    """
    sc_obj = sc()
    sc_obj.startcounttemp()  # temporary buffer for matches
    type_elements = []

    # Support simple edges (u, v, d) and other edge tuple shapes
    for edge in G.edges(data=True):
        if len(edge) == 3:
            u, v, d = edge
        else:
            u, v, *rest = edge
            d = rest[-1] if rest else {}
        label = d.get("label") if isinstance(d, dict) else None
        if v == type and label == bias:
            type_elements.append(u)

    sc_obj.subtemp()  # done with temporary buffer
    if not type_elements:
        space_used = sc_obj.get_max()
        if return_space:
            return (None, space_used)
        return None

    val = random.choice(type_elements)
    space_used = sc_obj.get_max()
    if return_space:
        return (val, space_used)
    return val

def implement(FUN, N, return_space: bool = False):
    """Call FUN N times and return a list of results (tracks space)."""
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent results
    results = []
    for _ in range(N):
        sc_obj.startcounttemp()  # iteration temporary
        results.append(FUN())
        sc_obj.subtemp()
    space_used = sc_obj.get_max()
    if return_space:
        return (results, space_used)
    return results

def write_all(S, bias, type, return_space: bool = False):
    """Collect all elements from S matching getattr(element, bias) == type."""
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent result
    result = []
    for element in S:
        sc_obj.startcounttemp()  # element temporary
        if getattr(element, bias) == type:
            pair(result, element)   # pair is in-place
        sc_obj.subtemp()
    space_used = sc_obj.get_max()
    if return_space:
        return (result, space_used)
    return result

# Additional functions

def list_create(M, return_space: bool = False):
    """Create a blank list with slots for M items"""
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent list
    result = [None] * M
    space_used = sc_obj.get_max()
    if return_space:
        return (result, space_used)
    return result

def merge(I, J, return_space: bool = False):
    """Merge two items I and J to create a list"""
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent merged list
    result = [I, J]
    space_used = sc_obj.get_max()
    if return_space:
        return (result, space_used)
    return result

def remove_item(I, L, return_space: bool = False):
    sc_obj = sc()
    sc_obj.startcounttemp()  # persistent result
    result = L.copy()
    if I in result:
        result.remove(I)
    space_used = sc_obj.get_max()
    if return_space:
        return (result, space_used)
    return result

def dim_set(D):
    def classify(items, dimension_func=D, return_space: bool = False):
        sc_obj = sc()
        sc_obj.startcounttemp()  # persistent result set
        result = set()
        for item in items:
            sc_obj.startcounttemp()  # small temporary
            result.add(dimension_func(item))
            sc_obj.subtemp()
        space_used = sc_obj.get_max()
        if return_space:
            return (result, space_used)
        return result
    return classify

def write_all_set(S, return_space: bool = False):
    """Write all items belonging to a particular set S as a sorted string."""
    sc_obj = sc()
    sc_obj.startcounttemp()  # temporary sorting buffer
    out = " - ".join(sorted(S))
    sc_obj.subtemp()
    space_used = sc_obj.get_max()
    if return_space:
        return (out, space_used)
    return out
