import primitive_fucntions as pf
import time
import tracemalloc
from collections import defaultdict
from utils import Stopwatch
from itertools import chain


def find_bias(S,clock):
    bias = None
    attribute_counts = {attr: len(set(getattr(obj, attr) for obj in S)) 
                   for attr in ["attribute1", "attribute2"]}
    # Count unique values for both attributes
    # Select the attribute with exactly 2 types while the other has != 2 types
    if attribute_counts["attribute1"] == 2 and attribute_counts["attribute2"] != 2:
        bias = "attribute1"
    elif attribute_counts["attribute2"] == 2 and attribute_counts["attribute1"] != 2:
        bias = "attribute2"
    else:
        clock.start()
        bias = "attribute1" if pf.flip(0.5) else "attribute2"  # Default random selection
        clock.stop()
    return bias

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
        sorter = getattr(element, bias)  # Dynamically get the attribute value
        chunks[sorter].append(element)
        pf.setminus(S, element)
    stopwatch.stop()
    n = len(chunks) # reassign n
    stopwatch.start()
    result = []
    for _ in range(n):
        chunk = pf.sample(chunks)
        result = pf.append(result, chunk)
        pf.setminus(chunks, chunk)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()

    return (result, time_elapsed)

def palindrome(S):
    # preprocessing (not part of measured cognitive process)
    n = len(S) / 2 # number of elements in basis
    stopwatch = Stopwatch()
    # select attribute which chunking is based on
    bias = find_bias(S)
    basis = []
    result = []
    for _ in range(n):
        element = pf.sample(S)
        type_ = getattr(element, bias)
        if type_ not in basis: # ends up being more probabilistic than it should be;
            basis.append(type_)
        else:
            _+=1 # amortized O(<2n)
            continue 
        result = pf.append(result, element)
        pf.setminus(element)
    for _ in range(n):
        element = pf.write_random(S, bias, basis[n-1-_])
        



def alternate(S):
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

def seriate(S):
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

