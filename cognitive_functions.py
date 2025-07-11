import primitive_fucntions as pf
from collections import defaultdict
from utils import Stopwatch, ElementSet, Associations

# --- Cognitive Functions using Graph Node Structure --- #

def iterate(S: ElementSet):
    n = len(S.elements)
    chunks = defaultdict(list)
    stopwatch = Stopwatch()

    bias = find_bias(S, stopwatch)
    for _ in range(n // 2):
        element = pf.sample(S.elements)

    bias = find_bias(S, stopwatch)
    stopwatch.start()
    for _ in range(n):
        element = pf.sample(S.elements)
        sorter = getattr(element, bias)
        chunks[sorter].append(element)
        pf.setminus(S.elements, element)
    stopwatch.stop()

    chunks = {tuple(v) for v in chunks.values()}
    stopwatch.start()
    result = []
    for _ in range(len(chunks)):
        chunk = pf.sample(chunks)
        stopwatch.stop()
        temp = list(chunk)
        stopwatch.start()
        result = pf.append(result, temp)
        pf.setminus(chunks, chunk)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    return (result, time_elapsed)

def palindrome(S: ElementSet):
    n = len(S.elements) // 2
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch)
    stopwatch.start()
    basis, rev = [], []

    while len(S.elements) > n:
        element = pf.sample(S.elements)
        if len(basis) == 0 or not any(pf.check_if_same_type(element, chosen, bias) for chosen in basis):
            pf.pair(basis, element)
            pf.setminus(S.elements, element)

    for i in range(n):
        target_type = getattr(basis[n - 1 - i], bias)
        candidates = [u for u, v, d in S.graph.edges(data=True) if v == target_type and d['label'] == bias and u in S.elements]
        if candidates:
            element = pf.sample(candidates)
            pf.pair(rev, element)
            pf.setminus(S.elements, element)

    result = pf.append(basis, rev)
    stopwatch.stop()
    return (result, stopwatch.get_elapsed_time())

def alternate(S: ElementSet):
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, two_flag=True)
    result = []

    while len(S.elements) > 0:
        element = pf.sample(S.elements)
        if len(result) == 0 or not pf.check_if_same_type(element, result[-1], bias):
            pf.pair(result, element)
            pf.setminus(S.elements, element)

    return (result, stopwatch.get_elapsed_time())

def chaining(S: ElementSet, associations: Associations):
    stopwatch = Stopwatch()
    stopwatch.start()
    chunks = []
    result = []

    while len(S.elements) > 0:
        element = pf.sample(S.elements)
        if element in associations.associations:
            chunk = []
            pf.pair(chunk, element)
            pf.setminus(S.elements, element)

            while True:
                next_element = pf.sample(S.elements)
                if next_element == associations.associations[element]:
                    pf.pair(chunk, next_element)
                    pf.setminus(S.elements, next_element)
                    pf.pair(chunks, chunk)
                    break

    result = chunks
    stopwatch.stop()
    return (result, stopwatch.get_elapsed_time())

def seriate(S: ElementSet):
    #  123123
    pass

def serial_crossed(S: ElementSet):
    n = len(S.elements) // 2
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, higher_dim=True)
    result = []

    while len(S.elements) > n:
        element = pf.sample(S.elements)
        if len(result) == 0 or pf.check_if_same_type(element, result[-1], bias[0]):
            pf.pair(result, element)
            pf.setminus(S.elements, element)

    for i in range(n):
        target_type = getattr(result[i], bias[1])
        candidates = [u for u, v, d in S.graph.edges(data=True) if v == target_type and d['label'] == bias[1] and u in S.elements]
        if candidates:
            element = pf.sample(candidates)
            pf.pair(result, element)
            pf.setminus(S.elements, element)

    return (result, stopwatch.get_elapsed_time())

def center_embedded(S: ElementSet):
    n = len(S.elements) // 2
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, higher_dim=True)
    result = []

    while len(S.elements) > 0:
        element = pf.sample(S.elements)
        if len(result) == 0 or pf.check_if_same_type(element, result[-1], bias[0]):
            pf.pair(result, element)
            pf.setminus(S.elements, element)
        if len(result) == n:
            break

    for i in range(n):
        target_type = getattr(result[n - 1 - i], bias[1])
        candidates = [u for u, v, d in S.graph.edges(data=True) if v == target_type and d['label'] == bias[1] and u in S.elements]
        if candidates:
            element = pf.sample(candidates)
            pf.pair(result, element)
            pf.setminus(S.elements, element)

    stopwatch.stop()
    return (result, stopwatch.get_elapsed_time())

def tail_recursive(S: ElementSet):
    stopwatch = Stopwatch()
    bias = find_bias(S, stopwatch, two_flag=True, higher_dim=True)
    stopwatch.start()
    result = []

    while len(S.elements) > 0:
        element = pf.sample(S.elements)
        pf.setminus(S.elements, element)
        target_type = getattr(element, bias[0])
        candidates = [u for u, v, d in S.graph.edges(data=True) if v == target_type and d['label'] == bias[0] and u in S.elements]
        if candidates:
            paired_element = pf.sample(candidates)
            result = pf.append(result, pf.merge(element, paired_element))
            pf.setminus(S.elements, paired_element)

    stopwatch.stop()
    return (result, stopwatch.get_elapsed_time())

def find_bias(S, clock, two_flag=False, higher_dim=False):
    if isinstance(S, ElementSet):
        elements = S.elements
    else:
        elements = S

    if higher_dim:
        attribute_counts = {
            attr: len(set(getattr(obj, attr) for obj in elements))
            for attr in ["attribute1", "attribute2"]
        }
        chunk_bias = find_bias(elements, clock, two_flag)
        clock.start()
        serial_bias = 'attribute1' if chunk_bias == 'attribute2' else 'attribute2'
        clock.stop()
        return (chunk_bias, serial_bias)
    else:
        attribute_counts = {
            attr: len(set(getattr(obj, attr) for obj in elements))
            for attr in ["attribute1", "attribute2"]
        }
        if attribute_counts["attribute1"] == 2 and attribute_counts["attribute2"] != 2:
            return "attribute1"
        elif attribute_counts["attribute2"] == 2 and attribute_counts["attribute1"] != 2:
            return "attribute2"
        else:
            clock.start()
            bias = "attribute1" if pf.flip(0.5) else "attribute2"
            clock.stop()
            return bias
