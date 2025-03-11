import primitive_fucntions as pf
import time
import tracemalloc
from collections import defaultdict
from utils import Stopwatch
from itertools import chain

# 1-D

def chunk(S):
    # preprocessing (not part of measured cognitive process)
    n = len(S) # number of elements in the set
    chunks = defaultdict(list) 
    stopwatch = Stopwatch()
    # --- #
    # select attribute which chunking is based on
    stopwatch.start()
    chunker = (
        'attribute1' 
        if any(getattr(obj, 'attribute2') is None for obj in S or pf.flip(0.5)) 
        else 'attribute2'
    )
    for _ in range(n):
        element = pf.sample(S) # select an element in the set
        sorter = getattr(element, chunker)  # Dynamically get the attribute value
        chunks[sorter].append(element)
        pf.setminus(S, element)
    stopwatch.stop()
    n = len(chunks) # reassign n
    stopwatch.start
    result = []
    for _ in range(n):
        chunk = pf.sample(chunks)
        pf.append(result, chunk)
        pf.setminus(chunks, chunk)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()

    return (result, time_elapsed)

def palindrome(S):
    if pf.flip(0.5):
        pass
    else:
        pass
    return


def alternate(S):
    if pf.flip(0.5):
        pass
    else:
        pass
    return
    return

# 2-D

def serial_crossed(S):
    return

def center_embedded(S):
    return

def pair(S):
    return

