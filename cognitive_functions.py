import primitive_fucntions as pf
from collections import defaultdict
from utils import Stopwatch, Element, ElementSet, Associations, SpaceComplexity
 
# 1-D

def iterate(S: ElementSet):     # 112233    
    items = _items_from_S(S)
    sc_obj = SpaceComplexity()

    # preprocessing (not part of measured cognitive process)
    n = len(items) # number of elements in the set

    # persistent container: chunks
    sc_obj.startcounttemp()
    chunks = defaultdict(list)
    stopwatch = Stopwatch()

    bias = find_bias(items, stopwatch)
    for _ in range(n//2):
        _ = pf.sample(items)

    bias = find_bias(items, stopwatch)
    stopwatch.start()
    for _ in range(n):
        element = pf.sample(items) # select an element in the set
        sorter = getattr(element, bias)
        chunks[sorter].append(element)
        pf.setminus(items, element)
    stopwatch.stop()
    sc_obj.startcounttemp()
    n_chunks = len(chunks) # reassign n
    chunks_set = {tuple(v) for k, v in chunks.items()}

    sc_obj.startcounttemp()
    result = []
    stopwatch.start()
    for _ in range(n_chunks):
        chunk = pf.sample(chunks_set)
        sc_obj.startcounttemp()
        temp = list(chunk)
        sc_obj.subtemp()
        result = pf.append(result, temp)
        pf.setminus(chunks_set, chunk)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    space_used = sc_obj.get_max()

    return (result, time_elapsed, space_used)

def palindrome(S):
    items = _items_from_S(S)
    sc_obj = SpaceComplexity()

    # preprocessing (not part of measured cognitive process)
    n = len(items) // 2 # number of elements in basis
    stopwatch = Stopwatch()

    # select attribute which chunking is based on
    bias = find_bias(items, stopwatch)
    stopwatch.start()

    sc_obj.startcounttemp()
    basis = []
    sc_obj.startcounttemp()
    rev = []

    # write_random() fallback implementation:
    def _pick_matching_element(pool, attr, value):
        sc_obj.startcounttemp()
        candidates = [e for e in pool if getattr(e, attr) == value]
        sc_obj.subtemp()
        if not candidates:
            return None
        return pf.sample(set(candidates))

    while len(items) > n:
        element = pf.sample(items)
        if len(basis)==0 or not any(getattr(element, bias) == getattr(chosen, bias) for chosen in basis):
            pf.pair(basis, element)
            pf.setminus(items, element)

    for _ in range(n):
        target_type = getattr(basis[n-1-_], bias)
        element = None
        try:
            candidate = pf.write_random(items, bias, target_type)
        except Exception:
            candidate = None
        if candidate:
            element = candidate
        else:
            element = _pick_matching_element(items, bias, target_type)
            if element is None:
                if len(items) == 0:
                    break
                element = pf.sample(items)
        pf.pair(rev, element)
        pf.setminus(items, element)

    result = pf.append(basis, rev)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    space_used = sc_obj.get_max()

    return (result, time_elapsed, space_used)      

def alternate(S):
    items = _items_from_S(S)
    sc_obj = SpaceComplexity()
    stopwatch = Stopwatch()

    sc_obj.startcounttemp()
    result = []

    # select attribute which chunking is based on
    bias = find_bias(items, stopwatch, two_flag=True)
    stopwatch.start()
    while len(items) > 0:
        element = pf.sample(items)
        if len(result) == 0 or not (getattr(element, bias) == getattr(result[-1], bias)):
            pf.pair(result, element)    
            pf.setminus(items, element)
        else:
            # skip and try again
            continue
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    space_used = sc_obj.get_max()

    return (result, time_elapsed, space_used)

def chaining(S, associations: dict):
    items = _items_from_S(S)
    sc_obj = SpaceComplexity()
    stopwatch = Stopwatch()

    sc_obj.startcounttemp()
    chunks = []
    stopwatch.start()
    while len(items) > 0:
        element = pf.sample(items)
        if element in associations.keys():
            sc_obj.startcounttemp()  # chunk persisted inside chunks
            chunk = []
            pf.pair(chunk, element)
            pf.setminus(items, element)
            while True:
                if len(items) == 0:
                    break
                next_element = pf.sample(items)
                if next_element == associations[element]:
                    pf.pair(chunk, next_element)
                    pf.setminus(items, next_element)
                    pf.pair(chunks, chunk)
                    break
                else:
                    continue
        else:
            # element had no association; skip it
            continue
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    space_used = sc_obj.get_max()

    return (chunks, time_elapsed, space_used)

def seriate(S):
    #  123123
    pass

# -------- 2-D -------- #

def serial_crossed(S):
    items = _items_from_S(S)
    sc_obj = SpaceComplexity()
    stopwatch = Stopwatch()

    n = len(items) // 2 # number of elements in the basis

    bias = find_bias(items, stopwatch, higher_dim=True)

    sc_obj.startcounttemp()
    result = []

    stopwatch.start()
    while len(items) > n:
        element = pf.sample(items)
        if len(result) == 0 or getattr(element, bias[0]) == getattr(result[-1], bias[0]):
            pf.pair(result, element)
            pf.setminus(items, element)

    for _ in range(n):
        target_type = getattr(result[_], bias[1])
        chosen = None
        try:
            chosen = pf.write_random(items, bias[1], target_type)
        except Exception:
            chosen = None
        if not chosen:
            sc_obj.startcounttemp()
            candidates = [e for e in items if getattr(e, bias[1]) == target_type]
            sc_obj.subtemp()
            chosen = pf.sample(set(candidates)) if candidates else None
            if chosen is None:
                if len(items) == 0:
                    break
                chosen = pf.sample(items)
        pf.pair(result, chosen)
        pf.setminus(items, chosen)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    space_used = sc_obj.get_max()
    return (result, time_elapsed, space_used)

def center_embedded(S):
    items = _items_from_S(S)
    sc_obj = SpaceComplexity()
    stopwatch = Stopwatch()

    n = len(items) // 2
    bias = find_bias(items, stopwatch, higher_dim=True)

    sc_obj.startcounttemp()
    result = []

    stopwatch.start()
    while len(items) > 0:
        element = pf.sample(items)
        if len(result) == 0 or getattr(element, bias[0]) == getattr(result[-1], bias[0]):
            pf.pair(result, element)
            pf.setminus(items, element)

    for _ in range(n):
        target_type = getattr(result[n - 1 - _], bias[1])
        # try write_random
        chosen = None
        try:
            chosen = pf.write_random(items, bias[1], target_type)
        except Exception:
            chosen = None
        if not chosen:
            sc_obj.startcounttemp()
            candidates = [e for e in items if getattr(e, bias[1]) == target_type]
            sc_obj.subtemp()
            chosen = pf.sample(set(candidates)) if candidates else None
            if chosen is None:
                if len(items) == 0:
                    break
                chosen = pf.sample(items)
        pf.pair(result, chosen)
        pf.setminus(items, chosen)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    space_used = sc_obj.get_max()
    return (result, time_elapsed, space_used)

def tail_recursive(S):
    items = _items_from_S(S)
    sc_obj = SpaceComplexity()
    stopwatch = Stopwatch()

    bias = find_bias(items, stopwatch, two_flag=True, higher_dim=True)
    stopwatch.start()

    sc_obj.startcounttemp()
    result = []

    while len(items) > 0:
        element = pf.sample(items)
        pf.setminus(items, element)
        target_type = getattr(element, bias[0])
        # try write_random / fallback
        paired_element = None
        try:
            paired_element = pf.write_random(items, bias[0], target_type)
        except Exception:
            paired_element = None
        if not paired_element:
            sc_obj.startcounttemp()
            candidates = [e for e in items if getattr(e, bias[0]) == target_type]
            sc_obj.subtemp()
            paired_element = pf.sample(set(candidates)) if candidates else None
            if paired_element is None:
                if len(items) == 0:
                    break
                paired_element = pf.sample(items)
        result = pf.append(result, pf.merge(element, paired_element))
        pf.setminus(items, paired_element)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    space_used = sc_obj.get_max()
    return (result, time_elapsed, space_used)


# ---------------------------------------------------------------------#

# utils

def find_bias(S,clock,two_flag=False,higher_dim=False):
    """
    Count unique values for both attributes, 
    select the attribute with exactly 2 types while the other has != 2 types

    Input Arguments:
        S: set of elements to be experimented with
        clock: stopwatch used to time primitive functions
        two_flag: flag to indicate if the bias required needs only two attribute types
        higher_dim: flag to indicate if the set of elements is 2-dimensional

    Output:
        bias: the bias lol, the attribute the flip selected
    """
    if higher_dim == True:
        chunk_bias, serial_bias = None, None
        attribute_counts = {attr: len(set(getattr(obj, attr) for obj in S)) 
                    for attr in ["attribute1", "attribute2"]}
        chunk_bias = find_bias(S, clock, two_flag)
        clock.start()
        serial_bias = 'attribute1' if chunk_bias == 'attribute2' else 'attribute2'
        clock.stop()
        return (chunk_bias, serial_bias)
    else:
        bias = None
        attribute_counts = {attr: len(set(getattr(obj, attr) for obj in S)) 
                    for attr in ["attribute1", "attribute2"]}
        if attribute_counts["attribute1"] == 2 and attribute_counts["attribute2"] != 2:
            bias = "attribute1" if not two_flag else "attribute1"
        elif attribute_counts["attribute2"] == 2 and attribute_counts["attribute1"] != 2:
            bias = "attribute2" if not two_flag else "attribute1"
        else:
            clock.start()
            bias = "attribute1" if pf.flip(0.5) else "attribute2"  # Default random selection
            clock.stop()
        return bias