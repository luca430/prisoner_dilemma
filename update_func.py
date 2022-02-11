import numpy as np
import numpy.random as npr

def update_1(h,strat,av): #taglia la testa al toro

    h1 = []
    perc = np.array([av[i]/np.sum(av) for i in range(len(strat))])

    for i in range(len(strat)):
        for j in range(int(round(len(h)*perc[i],0))):
            h1.append(strat[i])
    
    while len(h1) != len(h):
        if len(h1) > len(h): h1.remove(strat[int(np.where(perc == np.min(perc))[0])])
        elif len(h1) < len(h): h1.append(strat[int(np.where(perc == np.max(perc))[0])])

    return np.sort(np.array(h1))

def update_1rand(h,strat,av): 

    h1 = []
    perc = np.array([av[i]/np.sum(av) for i in range(len(strat))])

    for i in range(len(strat)):
        for j in range(int(round(len(h)*perc[i],0))):
            h1.append(strat[i])
    
    while len(h1) != len(h):
        if len(h1) > len(h): h1.remove(strat[int(np.where(perc == np.min(perc))[0])])
        elif len(h1) < len(h): h1.append(strat[int(np.where(perc == np.max(perc))[0])])
    
    h1[npr.randint(len(h1))] = npr.randint(5) #numero di strategie (da aggiungere in input?)

    return np.sort(np.array(h1))

def update_2(h,strat,av):
    if len(h)<20:
        if len(strat)<3: w=0
        else: w=npr.randint(2)
        k=np.where(h==strat[w])[0]
        if len(k)<1:
            return h
        else:
            h[k[0]]=strat[-w-1]
    else:
        for i in range(3):
            if len(av)<1: break
            else:
                if len(strat)<3: w=0
                else: w=npr.randint(2)   
                k=np.where(h==strat[w])[0]
            if len(k)<1: break
            else:h[k[0]]=strat[-npr.randint(2)-1]

    return np.sort(np.array(h))
def update_3(h,strat,av):
    K=0.83
    if len(strat)<2: return h
    else:
        x=[npr.randint(len(strat)) for i in range(2)]
        P=[np.where(strat==x[0])[0],np.where(strat==x[1])[0]]
        #strategie opposte
        p_loc=1/(1+np.exp(-(P[0]-P[1])/K)) #probabilità che x vada a y strategia
        j=np.where(h==strat[np.where(av==P[0])[0]])[0]
        j=j[:int(len(j)*p_loc)]
        for i in j:
            h[i]=strat[np.where(av==P[1])[0]]
        return np.sort(np.array(h))
