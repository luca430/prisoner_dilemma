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
    
def grim(it,u,v,u2):
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
        
def sus_tit_tat(it,u,v,u2):
    if it==2: return ud
    else: return u
    
def pavlov(it,u,v,u2):
    if u == v: return uc
    else: return ud
    
def reactive_nice(it,u,v,u2):
    y = 0.5
    p = 0.7
    if it == 2:
        if npr.random() <= y: return uc
        else: return ud
    else:
        if u == uc:
            if npr.random() <= p: return uc
            else: return ud
        else:
            if npr.random() <= 1-p: return uc
            else: return ud
    
def reactive_bad(it,u,v,u2):
    y = 0.5
    p = 0.3
    if it == 2:
        if npr.random() <= y: return uc
        else: return ud
    else:
        if u == uc:
            if npr.random() <= p: return uc
            else: return ud
        else:
            if npr.random() <= 1-p: return uc
            else: return ud 
            
def hard_joss(it,u,v,u2):
    p = 0.9
    if it==2: return uc
    else:
        if u == uc:
            if npr.random() <= p: return uc
            else: return ud
        else: return ud
        
def soft_joss(it,u,v,u2):
    p = 0.9
    if it==2: return uc
    else:
        if u == ud:
            if npr.random() <= p: return ud
            else: return uc
        else: return uc