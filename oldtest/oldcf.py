import oldpf as pf
from collections import defaultdict
from oldutils import Stopwatch, Element, ElementSet, Associations
 
# 1-D

def iterate(S):     # 112233    

    # preprocessing (not part of measured cognitive process)
    n = len(S) # number of elements in the set
    chunks = defaultdict(list) 
    stopwatch = Stopwatch()
    # --- #
    # select attribute which chunking is based on

    ### ADD CODE HERE
    """ graph algo here"""
    bias = find_bias(S, stopwatch)
    for _ in range(n//2):
        element = pf.sample(S)
    result = None
    time_elapsed = None


    # """ non graph algo here"""
    bias = find_bias(S, stopwatch)
    stopwatch.start()
    for _ in range(n):
        element = pf.sample(S) # select an element in the set
        sorter = getattr(element, bias)
        chunks[sorter].append(element)
        pf.setminus(S, element)
    stopwatch.stop()
    n = len(chunks) # reassign n
    chunks = {tuple(v) for k, v in chunks.items()}
    stopwatch.start()
    result = []
    for _ in range(n):
        chunk = pf.sample(chunks)
        stopwatch.stop()
        temp = list(chunk)
        stopwatch.start()
        result = pf.append(result, temp)
        pf.setminus(chunks, chunk)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()

    return (result, time_elapsed)

def palindrome(S):
    # 123321
    # preprocessing (not part of measured cognitive process)
    n = len(S) // 2 # number of elements in basis
    stopwatch = Stopwatch()
    # select attribute which chunking is based on
    bias = find_bias(S, stopwatch)
    stopwatch.start()
    basis, rev = [], []
    # write_random() based implementation
    ### WRITE CODE HERE
    while (len(S) > n):
        element = pf.sample(S)
        if len(basis)==0 or not (any(pf.check_if_same_type(element, chosen, bias) for chosen in basis)):
            pf.pair(basis, element)
            pf.setminus(S, element)
    for _ in range(n):
        element = pf.write_random(S, bias, getattr(basis[n-1-_], bias))
        pf.pair(rev,element)
        pf.setminus(S, element)
    result = pf.append(basis,rev)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    
    return (result, time_elapsed)  

def alternate(S):
    # 121212
    # preprocessing (not part of measured cognitive process)
    n = len(S) # number of elements in the set
    stopwatch = Stopwatch()
    # --- #
    # select attribute which chunking is based on
    ### ADD CODE HERE
    ### subject knows what types of attributes are there
    ### and what type of attribute to select

    bias = find_bias(S,stopwatch,two_flag=True)
    result = []
    while (len(S) > 0):
        element = pf.sample(S)
        if len(result) == 0 or not pf.check_if_same_type(element, result[-1], bias):
            pf.pair(result, element)    
            pf.setminus(S, element)
    time_elapsed = stopwatch.get_elapsed_time()

    return (result, time_elapsed)

def chaining(S, associations: dict):
    # preprocessing (not part of measured cognitive process)
    n = len(S) # number of elements in the set
    stopwatch = Stopwatch()
    # --- #
    stopwatch.start()
    chunks = []
    result = []
    while (len(S) > 0):
        element = pf.sample(S)
        if element in associations.keys():
            chunk = []
            pf.pair(chunk, element)
            pf.setminus(S, element)
            while True:
                next_element = pf.sample(S)
                if next_element == associations[element]:
                    pf.pair(chunk, next_element)
                    pf.setminus(S, next_element)
                    pf.pair(chunks, chunk)
                    break
                else:
                    continue
        else:
            continue
    result = chunks
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()

    return  (result, time_elapsed)

def seriate(S):
    #  123123
    pass

# -------- 2-D -------- #

def serial_crossed(S):
    n = len(S) // 2 # number of elements in the basis
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, higher_dim=True)
    result = []
    while len(S) > n:
        element = pf.sample(S)
        if len(result) == 0 or pf.check_if_same_type(element, result[-1], bias[0]):
            pf.pair(result, element)
            pf.setminus(S, element)
    for _ in range(n):
        element = pf.write_random(S, bias[1], getattr(result[_], bias[1]))
        pf.pair(result, element)
        pf.setminus(S, element)
    time_elapsed = stopwatch.get_elapsed_time()
    return (result, time_elapsed)



def center_embedded(S):
    n = len(S) // 2 # number of elements in the basis
    # 
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, higher_dim=True)
    result = []
    while len(S) > 0:
        element = pf.sample(S)
        if len(result) == 0 or pf.check_if_same_type(element, result[-1], bias[0]):
            pf.pair(result, element)
            pf.setminus(S, element)
        if len(result) == n:
            break
    for _ in range(n):
        element = pf.write_random(S, bias[1], getattr(result[n - 1 - _], bias[1]))
        pf.pair(result, element)
        pf.setminus(S, element)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    return (result, time_elapsed)

'''

def center_embedded(S):
    n = len(S) // 2 
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, higher_dim=True)
    result = []

    while len(S) > 0:
        element = pf.sample(S)
        if len(result) == 0 or pf.check_if_same_type(element, result[-1], bias[0]):
            pf.pair(result, element)
            if element in S:
                pf.setminus(S, element)
            else:
                raise ValueError("[ERROR] Tried to remove an element not in S during first half.")
        if len(result) == n:
            break
    if len(result) < n:
        raise RuntimeError(f"[ERROR] Could not find enough matching elements for first half. Needed {n}, got {len(result)}")
    # Second half of the result
    if len(S) < n:
        raise RuntimeError(f"[ERROR] Not enough elements left in S to complete second half. Needed {n}, have {len(S)}")
    for _ in range(n):
        ref_attr = getattr(result[n - 1 - _], bias[1], None)
        if ref_attr is None:
            raise AttributeError(f"[ERROR] Element at position {n - 1 - _} has no attribute '{bias[1]}'")
        element = pf.write_random(S, bias[1], ref_attr)
        if element is None:
            raise ValueError(f"[ERROR] write_random() failed to find match for attribute '{ref_attr}'")
        pf.pair(result, element)
        if element in S:
            pf.setminus(S, element)
        else:
            raise ValueError("[ERROR] Tried to remove an element not in S during second half.")
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    return (result, time_elapsed)

'''

def tail_recursive(S):
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, two_flag=True, higher_dim=True)
    stopwatch.start()
    result = []
    while len(S) > 0:
        element = pf.sample(S)
        pf.setminus(S, element)
        paired_element = pf.write_random(S, bias[0], getattr(element, bias[0]))
        result = pf.append(result, pf.merge(element, paired_element))
        pf.setminus(S, paired_element)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    return (result, time_elapsed)


# ---------------------------------------------------------------------#

# utils

def find_bias(S,clock,two_flag=False,higher_dim=False):
    '''
    Count unique values for both attributes, 
    select the attribute with exactly 2 types while the other has != 2 types

    Input Arguments:
        S: set of elements to be experimented with
        clock: stopwatch used to time primitive functions
        two_flag: flag to indicate if the bias required needs only two attribute types
        higher_dim: flag to indicate if the set of elements is 2-dimensional

    Output:
        bias: the bias lol, the attribute the flip selected
    '''
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