import oldpf as pf
from oldutils import Stopwatch, Element, KComplexity

a = Element('A1','A','1')
b = Element('A2','A','2')
c = Element('B1','B','1')
d = Element('B2','B','2')

train_1 = {a,b,c,d}

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
    
kc = KComplexity()
result, time_elapsed = palindrome(train_1)
print(kc.get_k_complexity())
print(kc.get_prim_counts())
print("Result:", result)
print("Elapsed time:", time_elapsed)
