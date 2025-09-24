import pytest
from model.memory import (
    MemoryStructure, Token, Lexicon, List, Queue, Mode, Sequence, Pointer
)
import networkx as nx

def test_memorystructure_compute_weight_default():
    m = MemoryStructure()
    assert m.compute_weight() == 0.0

def test_token_init():
    t = Token(name="A", attribute1="x", attribute2="y")
    assert t.name == "A"
    assert t.attribute1 == "x"
    assert t.attribute2 == "y"
    assert isinstance(t.predecessors, set)
    assert isinstance(t.successors, set)

def test_lexicon_add_remove_token():
    t1 = Token(name="A")
    t2 = Token(name="B")
    lex = Lexicon(tokens=[t1])
    assert t1 in lex.tokens
    lex.add_token(t2)
    assert t2 in lex.tokens
    lex.remove_token(t1)
    assert t1 not in lex.tokens

def test_lexicon_compute_weight():
    t1 = Token(name="A")
    lex = Lexicon(tokens=[t1])
    assert isinstance(lex.compute_weight(), float)

def test_list_operations():
    l = List(items=[1,2,3])
    assert l.compute_weight() == 3
    l.suffix(4)
    assert l.items[-1] == 4
    l.prefix(0)
    assert l.items[0] == 0
    l.clear()
    assert len(l.items) == 0

def test_queue_operations():
    q = Queue(items=[1,2,3])
    assert q.compute_weight() == 3
    q.push_in(0)
    assert q.items[0] == 0
    out = q.push_out()
    assert out == 3
    q.clear()
    assert len(q.items) == 0

def test_mode_weight():
    m = Mode(item="test")
    assert m.compute_weight() == 1

def test_sequence_click():
    s = Sequence(items=[1])
    s.click(2)
    assert list(s.items) == [1,2]

def test_pointer_click():
    p = Pointer(items=[1])
    p.click(2)
    assert list(p.items) == [1,2]
