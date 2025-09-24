class wm():
    def __init__(self):    
        wm.value = 0
        wm_cache = []
    def update(self, value):
        wm.value += value
        wm_cache.append(wm.value)
    @property
    def max_space(self):
        return max(wm_cache)

def calculate_theoretical_complexity(algorithm, n, divs = None):
    kolmo = 0
    space = wm()
    if algorithm == 'chaning':
        pass
    if algorithm == 'ordinal':
        pass
    if algorithm == 'iterate':
        group = n / divs
        space.update(divs * (1 + 2*group)) #lexicon
        while(n):
            space.update(2) # current
            kolmo += 1 # current pf.sample
            kolmo += 1 # remove
            space.update(-2) # update lexicon
            n -= 1 # update lexicon
            # write_all
            # making find lexicon uses move so total space is not affected
            kolmo += (1 + (group - 1)*2) # find pf
            for _ in range(group - 2):
                kolmo += 3 # pfs: sample, add, remove
                space.update(-2)
                n -= 1
            kolmo += 2 # pfs: sample, add, remove for the last item
            space.update(-2) # remove last element from sub_lex
            space.update(-1) # remove attrbute node from sub_lex
            n -= 1
            space.update(-2) # purge current
        
    if algorithm == 'palindrome':
        space.update(divs * (1 + 2*group)) # lexicon
        for _ in range(n/2):
            kolmo += 1 # loop
            # sample current
            space.update(2)
            kolmo += 1 
            # add to basis
            kolmo += 1
            space.update(2)
            # remove from lexicon
            kolmo += 1
            space.update(-2)
            # pushing out to a diff lex
            kolmo += 2 # finding sublex
            kolmo += 0 # sample after finding
            kolmo += 2 # add, remove
            space.update(-2) # purge current
        basis = n/2
        for _ in range(n/2):
            kolmo += 1 # loop
            # push out from basis
            kolmo += 1 #space stays the same since it's being moved to remainder
            # iterate through basis, a queue
            remainder = 0
            while(basis):
                kolmo += 1 # loop
                # add to remainder
                kolmo += 1
                remainder += 1
                # push_out next
                kolmo += 1
                basis -= 1
            # write the other one
            kolmo += 1 # find and sample
            kolmo += 2 # add and remove
            basis = remainder
            space.update(-4) # removed from lexixon and basis
    
    if algorithm == 'alternate':
        space.update(divs * (1 + 2*group)) # lexicon
        # current
        kolmo += 1 # sample
        space.update(2)
        # remove from lexicon
        kolmo += 1
        space.update(-2)
        alternates = n/2
        for _ in range (n - 2):
            kolmo += 1 # loop
            # find_alternates
            kolmo += alternates
            # sample
            kolmo += 1
            # remove 
            kolmo += 1
            if _ % 2 == 0:
                alternates -= 1
            space.update(-2)
            if _ == n-3:
                space.update(-1) # remove the attribute node
        #getting rid of the last one
        kolmo += 1 #find the other one
        kolmo += 1 # remove
        space.update(-3) # remove token and the attr node from lexicon
    
    if algorithm == 'seriate':
        group = n/divs
        kolmo += (divs*3) 
        kolmo += divs*((group - 1)*(1 + 3) - 1) # for the write_all
        kolmo += (group - 1)*(1+1+1) # buffer except write random
        kolmo += ((group-1)*(group-2))/2 + (group-2) + 2*(group-1)



    if algorithm == 'serial-crossed':
        pass
    if algorithm == 'center-embedded':
        pass
    if algorithm == 'tail-recursive':
        pass
    
    return (kolmo, space.max_space)









