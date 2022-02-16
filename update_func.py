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


p_mut = 0

def update_2(h,strat,av,s,s_ref):

    h = np.array(h)
    new_strat = 0

    if np.shape(h) == (len(h.T),): #caso senza mutazione
        for i in range(3):
            if len(av)<1:break
            else:
                if len(strat)<3: w=0
                else: w=npr.randint(2)
                k=np.where(h==strat[w])[0] #???
                if len(k)<1:break
                else:h[k[0]]=strat[-w-1]
    
    else:                          #caso con mutazione
        for i in range(3):
            if len(av)<1:break
            else:
                if len(strat)<3: w=0
                else: w=npr.randint(2)
                k=np.where(h[0]==strat[w])[0]
                if len(k)<1:break
                else:h[0,k[0]]=strat[-w-1]

        for i in range(len(h)):
            if npr.random() < p_mut:
                #h[1,i] = npr.poisson(lam=0.01)
                h[1,i] = round(npr.random(),2)
                if h[1,i] > 1: h[1,i] = 1
                new_strat += 1
                s.append('{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100)))
                s_ref.append(h[:,i])

    return np.sort(np.array(h)), new_strat
