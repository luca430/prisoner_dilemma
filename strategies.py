import numpy.random as npr

uc, ud = [1,0], [0,1]
k=0.3

def nice_guy(it,u,v,u2):
    return uc

def bad_guy(it,u,v,u2):
    return ud

def mainly_nice(it,u,v,u2):
    a = npr.rand()
    if a > k: return uc
    else: return ud
    
def mainly_bad(it,u,v,u2):
    a = npr.rand()
    if a <= k: return uc
    else: return ud
    
def tit_tat(it,u,v,u2):
    if it==2: return uc
    else: return u
    
def random(it,u,v,u2):
    a = npr.rand()
    if a < 0.5: return uc
    else: return ud
    
def pavlov(it,u,v,u2):
    if it==2:
        return uc
    else:
        if v == ud:
            return ud
        else:
            if u == ud:
                return ud
            else: return uc

def f_tit_tat(it,u,v,u2):
    if it <= 3: return uc
    else:
        if u == ud and u2 == ud:
            return ud
        else: return uc
    
    
    
    
    
    