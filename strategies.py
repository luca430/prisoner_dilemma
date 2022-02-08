import numpy.random as npr

uc, ud = [1,0], [0,1]
k=0.3

def nice_guy(it,u):
    return uc
def bad_guy(it,u):
    return ud
def mainly_nice(it,u):
    a = npr.rand()
    if a > k: return uc
    else: return ud
def mainly_bad(it,u):
    a = npr.rand()
    if a <= k: return uc
    else: return ud
def tit_tat(it,u):
    if it==1: return uc
    else: return u 