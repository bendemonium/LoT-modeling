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
def add(L: mem.Lexicon | mem.Queue | mem.Sequence | mem.List, token):
    """adds a token to a list, or pushes it into a queue"""
    if isinstance(L, mem.List):
        L.suffix(token)
    if isinstance(L, mem.Sequence):
        L.click(token)
    if isinstance(L, mem.Queue):
        L.push_in(token)
    if isinstance(L, mem.Lexicon):
        L.add_token(token)
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
def sample(lexicon: mem.Lexicon):
    """Sample from a lexicon."""
    collection = list(lexicon.tokens)
    spit = random.choice(collection)
    weight = 0 if len(lexicon.tokens)==1 else 1
    return spit, weight

@primitive_function
def remove(lexicon: mem.Lexicon, T: mem.Token | mem.Lexicon):
    """Removes token from a lexicon"""
    weight = 0
    if isinstance(T, mem.Lexicon):
        for t in T.tokens:
            lexicon.remove_token(t)
            weight += 1
    else:
        lexicon.remove_token(T)
        weight += 1 
    return None, weight

@primitive_function
def inquire_token(token: mem.Token, bias, lexicon: mem.Lexicon | None = None):
    if bias == 'link':
        if lexicon.G.in_edges(token.name):
            value = 'in'
        else:
            value = 'out'
    else:
        value = getattr(token, bias)
    weight = 1
    return value, weight

@primitive_function
def find(lexicon: mem.Lexicon, token = None, criterion = None, *, negative = False, move = False):      
    if lexicon.linked == True:
        if criterion == 'in':
            pass
    else:
        if token:
            type_needed = inquire_token(token, criterion)
        else:
            type_needed = criterion
        found_elements = []
    if negative:
        for u, v in lexicon.G.edges():
            if lexicon.G.nodes[v].get("type") == criterion and v != type_needed and lexicon.G.nodes[u].get("type") == 'token':
                found_elements.append(u)
        weight = 1
    else:
        for u, v in lexicon.G.edges():
            if v == type_needed and lexicon.G.nodes[u].get("type") == 'token':
                found_elements.append(u)
        weight = 0
    sub_lex = mem.Lexicon()
    for token in lexicon.tokens:
        if token.name in found_elements:
            add(sub_lex, token)
    if move:
        remove(lexicon, sub_lex)
    return sub_lex, weight
    ##### fix this and subgraph lexes and try sets to reconstruct new instead of subgraph

@primitive_function
def check_similarity(e1, e2, bias):
    """Returns True if tokens are same type"""
    return getattr(e1,bias) == getattr(e2,bias), 1

@primitive_function
def write_random(lexicon: mem.Lexicon, token = None, bias = None, memory = None, criterion = None, found = False): 
    """Returns one unused member of particular type"""
    if found:
        collection = lexicon
    else:
        if token == None:
            collection = find(lexicon, criterion)
        else:
            collection = find(lexicon, bias, token)
    write = sample(collection)
    add(memory, write)
    remove(lexicon, write)
    weight = 0 if len(collection.tokens)==1 else 1
    return None, weight

@primitive_function
def write_all(lexicon, token, bias, memory):
    """Returns a sequential list of all tokens of a type"""
    sub_lex = find(lexicon, token, bias, move = True)
    while (sub_lex.tokens):
        write_random(sub_lex, token = token, bias = bias, memory = memory, found = True)
    weight = 0
    return None, weight

@primitive_function
def loop():
    weight = 1
    return None, weight

@primitive_function
def push_out(q: mem.Queue):
    token = q.push_out()
    weight = 2
    return token, weight