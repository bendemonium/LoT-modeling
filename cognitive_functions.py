import primitive_fucntions as pf
from collections import defaultdict
from utils import Stopwatch

# 1-D

def iterate(S):
    # preprocessing (not part of measured cognitive process)
    n = len(S) # number of elements in the set
    chunks = defaultdict(list) 
    stopwatch = Stopwatch()
    # --- #
    # select attribute which chunking is based on
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
        pf.append(result, temp)
        pf.setminus(chunks, chunk)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()

    return (result, time_elapsed)

def palindrome(S):
    # preprocessing (not part of measured cognitive process)
    n = len(S) // 2 # number of elements in basis
    stopwatch = Stopwatch()
    # select attribute which chunking is based on
    bias = find_bias(S, stopwatch)
    stopwatch.start()
    basis, rev = [], []
    for _ in range(n):
        element = pf.sample(S)
        print(_)
        if len(basis)==0 or not (any(pf.check_if_same_type(element, chosen, bias) for chosen in basis)):
            print(getattr(element, bias))
            pf.pair(basis, element)
            pf.setminus(S, element)
        else:
            i-=1
    for _ in range(n):
        print(n-1-_, len(basis))
        element = pf.write_random(S, bias, getattr(basis[n-1-_], bias))
        pf.pair(rev,element)
        pf.setminus(S, element)
    result = pf.append(basis,rev)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    
    return (result, time_elapsed)      

def alternate(S):
    # preprocessing (not part of measured cognitive process)
    n = len(S) # number of elements in the set
    stopwatch = Stopwatch()
    # --- #
    # select attribute which chunking is based on
    bias = find_bias(S,stopwatch)


    return

def seriate(S, associations: dict):
    # preprocessing (not part of measured cognitive process)
    n = len(S) # number of elements in the set
    stopwatch = Stopwatch()
    # --- #
    # select attribute which chunking is based on
    stopwatch.start()
    bias = (
        'attribute1' 
        if any(getattr(obj, 'attribute2') is None for obj in S or pf.flip(0.5)) 
        else 'attribute2'
    )
    return


# 2-D

def serial_crossed(S):
    
    return

def center_embedded(S):
    return

def pair(S):
    return


# ---------------------------------------------------------------------#

# utils

def find_bias(S,clock):
    """
    Count unique values for both attributes, 
    select the attribute with exactly 2 types while the other has != 2 types

    Input Arguments:
        S: set of elements to be experimented with
        clock: stopwatch used to time primitive functions

    Output:
        bias: the bias lol, the attribute the flip selected
    """
    bias = None
    attribute_counts = {attr: len(set(getattr(obj, attr) for obj in S)) 
                   for attr in ["attribute1", "attribute2"]}
    if attribute_counts["attribute1"] == 2 and attribute_counts["attribute2"] != 2:
        bias = "attribute1"
    elif attribute_counts["attribute2"] == 2 and attribute_counts["attribute1"] != 2:
        bias = "attribute2"
    else:
        clock.start()
        bias = "attribute1" if pf.flip(0.5) else "attribute2"  # Default random selection
        clock.stop()
    return bias