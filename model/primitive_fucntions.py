from dataclasses import dataclass
from functools import wraps
from contextvars import ContextVar
import inspect
from typing import Any, Callable, Dict, Optional, Tuple
import random
import model.memory as mem
from copy import deepcopy
from model.complexity import _CURRENT_RUN

SEED = 42
random.seed(SEED)

def primitive_function(pf):
    @wraps(pf)
    def pf_ize(*args, **kwargs):
        value, weight = pf(*args, **kwargs)
        scope = _CURRENT_RUN.get()
        if scope is not None:
            scope.kolmo.record(pf.__name__, weight)
        return value
    return pf_ize

@primitive_function
def add(L, token):
    """adds a token to a list, or pushes it into a queue"""
    if isinstance(L, mem.List):
        L.suffix(token)
    if isinstance(L, mem.Sequence):
        L.click(token)
    if isinstance(L, mem.Queue):
        L.push_in(token)
    weight = 1
    return None, weight

@primitive_function
def flip(p = 0.5):
    """Returns true with probability p"""
    weight = 1
    outcome = random.random() < p
    return outcome, weight

@primitive_function
def pick(a, b, p = 0.5):
    choice = a if flip(p) else b
    choice = mem.Mode(choice)
    weight = 0
    return choice, weight

@primitive_function
def sample(lexicon):
    """Sample from a lexicon."""
    collection = lexicon.tokens
    spit = deepcopy(random.sample(collection, 1)[0])
    weight = 0 if len(lexicon.tokens)==1 else 1
    return spit, weight

@primitive_function
def remove(lexicon, T):
    """Removes token from a lexicon"""
    if isinstance(T, mem.Lexicon):
        for t in T.tokens:
            remove(lexicon,t)
    lexicon.remove_token(T)
    weight = 1
    return None, weight

@primitive_function
def inquire_token(token, bias, lexicon = None):
    if bias == 'link':
        if lexicon.in_edges(token.name):
            value = 'in'
        else:
            value = 'out'
    else:
        value = getattr(token, bias)
    weight = 1
    return value, weight

@primitive_function
def find(lexicon, token = None, criterion = None, *, negative = False, move = False):      
    if lexicon.linked == True:
        if criterion == 'in':
            pass
    else:
        if token:
            type_needed = inquire_token(token, criterion)
        else:
            type_needed = criterion
    if negative:
        found_elements = [u for u, v, d in lexicon.edges(data=True) if v != type_needed and d["label"] == bias]
        weight = 1
    else:
        found_elements = [u for u, v, d in lexicon.edges(data=True) if v == type_needed and d["label"] == bias]
    weight += len(found_elements)
    sub_lex = {}
    for token in lexicon.tokens:
        if token.name in found_elements:
            sub_lex.add(token)
    sub_lex = mem.Lexicon(sub_lex)
    if move:
        remove(lexicon, sub_lex)
    return sub_lex, weight
    ##### fix this and subgraph lexes and try sets to reconstruct new instead of subgraph

@primitive_function
def check_similarity(e1, e2, bias):
    """Returns True if tokens are same type"""
    return getattr(e1,bias) == getattr(e2,bias)

@primitive_function
def write_random(lexicon, token = None, bias = None, memory = None, criterion = None, found = False): 
    """Returns one unused member of particular type"""
    if found:
        collection = lexicon
    else:
        if token == None:
            collection = find(lexicon, criterion)
        else:
            collection = find(lexicon, bias, token)
    write = sample(collection.elements, 1)
    add(memory, write)
    remove(lexicon, write)
    return None, weight

@primitive_function
def write_all(lexicon, token, bias, memory):
    """Returns a sequential list of all tokens of a type"""
    sub_lex = find(lexicon, token, bias, move = True)
    while (sub_lex.nodes):
        write_random(sub_lex, token = token, bias = bias, memory = memory, found = True)
    weight = 0
    return None, weight

@primitive_function
def loop():
    weight = 1
    return None, weight

@primitive_function
def push_out(q):
    token = q.push_out
    weight = 2
    return token, weight