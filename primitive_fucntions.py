import random

SEED = 42
random.seed(SEED)
# Functions on lists (strings)

def pair(L, C):
    """Concatenates character C onto list L
    Time complexity: O(1) amortized for lists, O(n) for strings"""
    L.append(C)   # O(1) amortized

def append(X, Y):
    """Append lists X and Y
    Time complexity: O(n+m) where n=len(X), m=len(Y)"""
    return X + Y

# Random functions

def flip(p):
    """Returns true with probability p
    Time complexity: O(1)"""
    return random.random() < p

# Set functions

# def union(set1, set2):
#     """Union of twos sets
#     Time complexity: O(len(set1) + len(set2))"""
#     return set1 | set2

def setminus(set1, s):
    """Remove a string from a set
    Time complexity: O(1) for single item, O(len(s)) for set s"""
    set1.remove(s)

def sample(set1):
    """Sample from a set of strings
    Time complexity: O(1) for non-empty sets"""
    if not set1:
        return None
    return random.sample(tuple(set1), 1)[0]

# Function calls with memoization

memoization_cache = {}
def F(z):
    """Generic factor function
    Time complexity: Depends on implementation"""
    pass

def Fm(z):
    """Memoized version of factor function
    Time complexity: O(1) for repeated calls"""
    if z not in memoization_cache:
        memoization_cache[z] = F(z)
    return memoization_cache[z]

# Token-related functions

def create_tokens():
    """Initiates a list of tokens [A1, A2, B3, B4]
    Time complexity: O(1)"""
    return ["A1", "A2", "B3", "B4"]

def add(T, list):
    """Adds token T to a list
    Time complexity: O(n) due to copying"""
    result = list.copy()
    result.append(T)
    return result

def remove(T, list):
    """Removes token T from a list
    Time complexity: O(n) for search and removal"""
    result = list.copy()
    if T in result:
        result.remove(T)
    return result

def check_if_same_type(e1, e2, bias):
    """Returns True if tokens are same type
    Time complexity: O(1)"""
    return getattr(e1,bias) == getattr(e2,bias)

def write_random(S, bias, type): 
    """Returns one unused member of particular type
    Time complexity: O(n) to filter tokens"""
    for element in S:
        if getattr(element, bias) == type:
            return element
        
        ### WRITE CODE
        ### maybe add a random list shuffling thing here
        ### to make it less predictable

    pass

def implement(FUN, N):
    """Keeps implementing a function N times
    Time complexity: O(N * T) where T is time of FUN"""
    results = []
    for _ in range(N):
        results.append(FUN())
    return results

def write_all(S, bias, type):
    """Returns a sequential list of all members of a type
    Time complexity: O(n) where n is number of tokens"""
    result = []
    for element in S:
        if getattr(element, bias) == type:
            result = pair(result, element)
    return result

# Additional functions

def list_create(M):
    """Create a blank list with slots for M items
    Time complexity: O(M)"""
    return [None] * M

def merge(I, J):
    """Merge two items I and J to create a list
    Time complexity: O(1)"""
    return [I, J]

def remove_item(I, L):
    """Remove item I from list L
    Time complexity: O(n) for search and removal"""
    result = L.copy()
    if I in result:
        result.remove(I)
    return result

def dim_set(D):
    """Create a set containing items classified by dimension D
    Time complexity: O(n*m) where n is number of items, m is time of D function"""
    def classify(items, dimension_func=D):
        result = set()
        for item in items:
            result.add(dimension_func(item))
        return result
    return classify

def write_all_set(S):
    """Write all items belonging to a particular set S
    Time complexity: O(n log n) due to sorting"""
    return " - ".join(sorted(S))