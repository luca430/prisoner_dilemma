import numpy as np
import numpy.random as npr

def lin1_icdf(x,l):
    return l - (2/l)*np.sqrt(1-x)

def lin2_icdf(x,l):
    return np.sqrt(x)/l

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

def update_2(h,strat,av,s,s_ref,p_mut = None,change=None):

    if p_mut == None: p_mut = 0
    if change == None: change = 1
    
    h = np.array(h)
    new_strat = 0

    if np.shape(h) == (len(h.T),): #caso senza mutazione
        for i in range(change):
            if len(strat)<=1:break
            else:
                if len(strat)<3: w=0
                else: 
                    w1=npr.randint(int(len(strat)/2))
                    w2=npr.randint(int(len(strat)/2),int(len(strat)))
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k=np.where(h==strat[w1])[0]
                    if len(k)<1:break
                    elif len(strat) == 1: break
                    else:h[k[0]]=strat[w2]
    
    else:                       #caso con mutazione
        for i in range(change):
            if len(strat.T)<=1: break
            else:
                if len(strat.T)<3: 
                    w1=0
                    w2=-1
                else: 
                    w1=npr.randint(int(len(strat.T)/2))  #only select killable strats among the worst half (center excluded)
                    w2=npr.randint(int(len(strat.T)/2),int(len(strat.T)))
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k = -1
                    for i in range(len(h[0])):
                        if np.all(h[:,i] == strat[:,w1]):
                            k = i
                            break
                    if k<0: break
                    else:
                        h[:,k]=strat[:,w2]

        for i in range(len(h)):
            if npr.random() < p_mut:
                #h[1,i] = npr.poisson(lam=0.01)
                h[1,i] = round(npr.random(),2)
                if h[1,i] > 1: h[1,i] = 1
                new_strat += 1
                s.append('{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100)))
                s_ref.append(h[:,i])

    return h, new_strat

def update_3(h,strat,av,s,s_ref,p_mut = None,change=None):

    if p_mut == None: p_mut = 0
    if change == None: change = 1
    
    h = np.array(h)
    new_strat = 0

    if np.shape(h) == (len(h.T),): #caso senza mutazione
        for i in range(change):
            if len(strat)<=1:break
            else:
                if len(strat)<3: 
                    w1=0
                    w2=-1
                else: 
                    x1,x2 = npr.random(),npr.random()
                    w1 = int(lin1_icdf(x1,len(strat)))
                    if w1 == len(strat)-1: w2 = w1
                    else: w2 = int(lin2_icdf(x2,(len(strat)-1)-w1)) + w1 + 1
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k=np.where(h==strat[w1])[0]
                    if len(k)<1:break
                    elif len(strat) == 1: break
                    else:h[k[0]]=strat[w2]
    
    else:                       #caso con mutazione
        for i in range(change):
            if len(strat.T)<=1: break
            else:
                if len(strat.T)<3: 
                    w1=0
                    w2=-1
                else: 
                    x1,x2 = npr.random(),npr.random()
                    w1 = int(lin1_icdf(x1,len(strat.T)))
                    if w1 == len(strat.T)-1: w2 = w1
                    else: w2 = int(lin2_icdf(x2,(len(strat.T)-1)-w1)) + w1 + 1
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k = -1
                    for i in range(len(h[0])):
                        if np.all(h[:,i] == strat[:,w1]):
                            k = i
                            break
                    if k<0: break
                    else:
                        h[:,k]=strat[:,w2]

        for i in range(len(h)):
            if npr.random() < p_mut:
                #h[1,i] = npr.poisson(lam=0.01)
                h[1,i] = round(npr.random(),2)
                if h[1,i] > 1: h[1,i] = 1
                new_strat += 1
                s.append('{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100)))
                s_ref.append(h[:,i])

    return h, new_strat