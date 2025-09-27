from __future__ import annotations
import model.memory as mem
import model.primitive_fucntions as pf
from model.complexity import _CURRENT_RUN, cognitive_function, Complexity


# 0D

def chaining(lexicon):
	sequence = mem.Sequence()
	pass

def ordinal(lexicon):
	sequence = mem.Sequence()
	pass


# 1D

@cognitive_function()
def iterate(lexicon):
	sequence = mem.Sequence()
	while(lexicon):
		current = pf.sample(lexicon)
		print(current)
		sequence.click(current)
		pf.remove(lexicon, current)
		pf.write_all(lexicon, current, 'attribute1', sequence)
		current.purge()
	return(sequence)

@cognitive_function()
def palindrome(lexicon):
	basis = mem.Queue()
	sequence = mem.Sequence()
	buffer = mem.Lexicon()
	while (lexicon):
		pf.loop()
		current = pf.sample(lexicon)
		pf.add(basis, current)
		pf.remove(lexicon, current)
		pf.write_all(lexicon, current, 'attribute1', buffer)
		sequence.click(current)
		current.purge()
	while(buffer):
		pf.loop()
		remainder = mem.Queue()
		base = pf.push_out(basis)
		while(basis):
			pf.loop()
			pf.add(remainder, base)
			base = pf.push_out(basis)
		pf.write_random(buffer, token = base, bias = 'attribute1', memory = sequence)
		basis.clone(remainder)
		remainder.purge()
		base.purge()
	return(sequence)

@cognitive_function()
def alternate(lexicon):
	sequence = mem.Sequence()
	current = pf.sample(lexicon)
	sequence.click(current)
	pf.remove(lexicon, current)
	while(lexicon):
		pf.loop()
		alternates = pf.find(lexicon, current, 'attribute1', negative = True)
		current.purge()
		current = pf.sample(alternates.tokens)
		sequence.click(current)
		pf.remove(lexicon, current)
	return(sequence)

@cognitive_function()	
def seriate(lexicon):
	sequence = mem.Sequence()
	basis = mem.Queue()
	buffer = mem.Lexicon()
	while(lexicon):
		pf.loop()
		current = pf.sample(lexicon)
		pf.add(basis, current)
		sequence.click(current)
		pf.write_all(lexicon, current, 'attribute1', buffer)
		current.purge()
	while(buffer):
		pf.loop()
		base = pf.push_out(basis)
		pf.write_random(buffer, base, 'attribute1', sequence)
		pf.add(basis, base)
		base.purge()
	return(sequence)

# 2D

@cognitive_function()
def serial_crossed(lexicon):
	sequence = mem.Sequence()
	bias1 = pf.pick('attribute1', 'attribute2')
	bias2 = mem.Mode('attribute1' if bias1 == 'attribute2' else 'attribute2')
	basis = mem.Queue()
	current = pf.sample(lexicon)
	sequence.click(current)
	pf.add(basis, current)
	pf.remove(current)
	buffer = pf.find(lexicon, current, bias1)
	current.purge()
	while(buffer):
		pf.loop()
		current = pf.sample(buffer.tokens)
		pf.add(basis, current)
		sequence.click(current)
		pf.remove(buffer, current)
		pf.remove(lexicon, current)
		current.purge()
	while(lexicon):
		pf.loop()
		base = pf.push_out(basis)
		pf.write_random(lexicon, basis, bias2, sequence)
		base.purge()
	return(sequence)

@cognitive_function()
def center_embedded(lexicon):
	sequence = mem.Sequence()
	bias1 = pf.pick('attribute1', 'attribute2')
	bias2 = mem.Mode('attribute1' if bias1 == 'attribute2' else 'attribute2')
	basis = mem.Queue()
	current = pf.sample(lexicon)
	sequence.click(current)
	pf.add(basis, current)
	pf.remove(current)
	buffer = pf.find(lexicon, current, bias1)
	current.purge()
	while(buffer):
		pf.loop()
		current = pf.sample(buffer)
		pf.add(basis, current)
		sequence.click(current)
		pf.remove(buffer, current)
		pf.remove(lexicon, current)
		current.purge()
	while(lexicon):
		pf.loop()
		remainder = mem.Queue()
		base = pf.push_out(basis)
		while(basis):
			pf.loop()
			pf.add(remainder, base)
			base = pf.push_out(basis)
		pf.write_random(buffer, token = base, bias = bias2, memory = sequence)
		basis.clone(remainder)
		remainder.purge()
		base.purge()
	return(sequence)

@cognitive_function()
def tail_recursive(lexicon): # head-tail
	sequence = mem.Sequence()
	bias1 = pf.pick('attribute1', 'attribute2')
	bias2 = mem.Mode('attribute1' if bias1 == 'attribute2' else 'attribute2')
	basis = mem.Queue()
	current = pf.sample(lexicon)
	sequence.click(current)
	pf.add(basis, current)
	buffer = pf.find(lexicon, current, bias1)
	while(buffer):
		pf.loop()
		current = pf.sample(buffer)
		pf.add(basis, current)
		sequence.click(current)
		pf.remove(buffer, current)
		pf.remove(lexicon, current)
		current.purge()
	buffer.purge()
	while(lexicon):
		pf.loop()
		base = pf.push_out(basis)
		buffer = pf.find(lexicon, base, bias2)
		current = pf.sample(lexicon)
		buffer.purge()
		pf.remove(lexicon, current)
		pf.add(basis, base)
		base.purge()
		buffer = pf.find(lexicon, current, bias1)
		current.purge()
		pf.remove(lexicon, buffer)
		while(buffer):
			pf.loop()
			base = pf.push_out()
			pf.write_random(buffer, base, bias2)
			pf.add(basis, base)
			base.purge()
		buffer.purge()
	return(sequence)































