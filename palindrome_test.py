from cognitive_functions import find_bias
from utils import Element, ElementSet, Stopwatch, KComplexity
import primitive_fucntions as pf

def palindrome(S: ElementSet):
    n = len(S.elements) // 2
    stopwatch = Stopwatch()
    bias = find_bias(S.elements, stopwatch)  
    stopwatch.start()
    basis, rev = [], []

    while len(S.elements) > n:
        element = pf.sample(S)
        if len(basis) == 0 or not any(pf.check_if_same_type(element, chosen, bias) for chosen in basis):
            pf.pair(basis, element)
            pf.setminus(S, element)

    for _ in range(n):
        element = pf.write_random(S, bias, getattr(basis[n-1-_], bias))
        pf.pair(rev, element)
        pf.setminus(S, element)

    result = pf.append(basis, rev)
    stopwatch.stop()
    time_elapsed = stopwatch.get_elapsed_time()
    return (result, time_elapsed)

e1 = Element("obj1", "red", "circle")
e2 = Element("obj2", "blue", "square")
e3 = Element("obj3", "red", "circle")
e4 = Element("obj4", "blue", "square")

element_set = ElementSet(elements=set([e1, e2, e3, e4]))

kc = KComplexity()

result, elapsed_time = palindrome(element_set)

print(kc.get_k_complexity())
print(kc.get_prim_counts())
print("Result:", result)
print("Elapsed time:", elapsed_time)