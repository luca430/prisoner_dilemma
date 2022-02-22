import numpy as np
import numpy.random as npr


def update_1(h,strat,av,s,s_ref,p_mut = None,change=None):
    new_strat = 0
    h=np.array(h)

    h1 = []

    new_strat = 0
    perc = np.array([av[i]/np.sum(av) for i in range(len(strat))])

    for i in range(len(strat)):
        for j in range(int(round(len(h)*perc[i],0))):
            h1.append(strat[i])
    
    while len(h1) != len(h):
        if len(h1) > len(h): h1.remove(strat[int(np.where(perc == np.min(perc))[0])])
        elif len(h1) < len(h): h1.append(strat[int(np.where(perc == np.max(perc))[0])])

    return np.array(h1), new_strat

def update_2(h,strat,av,s,s_ref,p_mut=None,change=None):

    if p_mut == None: p_mut = 0
    if change == None: change = 1
    
    h = np.array(h)
    new_strat = 0

    if np.shape(h) == (len(h.T),): #NO mutation
        for i in range(change):
            if len(strat) <= 1: break
            else:
                if len(strat) < 3:
                    w1 = 0
                    w2 = -1
                else: 
                    w1 = npr.randint(int(len(strat)/2))
                    w2 = npr.randint(int(len(strat)/2),int(len(strat)))
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k = np.where(h == strat[w1])[0]
                    if len(k) < 1:  break
                    elif len(strat) == 1:   break
                    else:   h[k[0]] = strat[w2]
    
    else:                       #YES mutation
        for i in range(change):
            if len(strat.T) <= 1: break
            else:
                if len(strat.T) < 3: 
                    w1 = 0
                    w2 = -1
                else: 
                    w1 = npr.randint(int(len(strat.T)/2))  #only select killable strats among the worst half (center excluded)
                    w2 = npr.randint(int(len(strat.T)/2),int(len(strat.T)))
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k = -1
                    for i in range(len(h[0])):
                        if np.all(h[:,i] == strat[:,w1]):
                            k = i
                            break
                    if k < 0: break
                    else:
                        h[:,k] = strat[:,w2]

        for i in range(len(h)):
            if npr.random() < p_mut:
                h[1,i] = round(npr.random(),2)
                if h[1,i] > 1: h[1,i] = 1
                new_strat += 1
                s.append('{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100)))
                s_ref.append(h[:,i])

    return h, new_strat

def update_3(h,strat,av,s,s_ref,p_mut=None,change=None):

    if p_mut == None: p_mut = 0
    if change == None: change = 1
    
    h = np.array(h)
    new_strat = 0

    def lin1_icdf(x,l):
        return l - l*np.sqrt(1-x)

    def lin2_icdf(x,l):
        return l*np.sqrt(x)

    if np.shape(h) == (len(h.T),): #NO mutation
        for i in range(change):
            if len(strat) <= 1:break
            else:
                if len(strat)<3: 
                    w1 = 0
                    w2 = -1
                else: 
                    x1,x2 = npr.random(),npr.random()
                    w1 = int(lin1_icdf(x1,len(strat)))
                    if w1 == len(strat)-1: w2 = w1
                    else:
                        w2 = len(strat)
                        while w2 == len(strat) or w2 == w1: #makes sure that w2 is not out of boundary and that it w2 != w1
                            w2 = int(lin2_icdf(x2,len(strat)-1-w1)) + w1 + 1
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k=np.where(h == strat[w1])[0]
                    if len(k) < 1:  break
                    elif len(strat) == 1: break
                    else:   h[k[0]] = strat[w2]
    
    else:                       #YES mutation
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
                    else:
                        w2 = len(strat.T)
                        while w2 == len(strat.T) or w2 == w1:   #makes sure that w2 is not out of boundary and that it w2 != w1
                            w2 = int(lin2_icdf(x2,(len(strat.T) - 1) - w1)) + w1 + 1
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
                h[1,i] = round(npr.random(),2)
                if h[1,i] > 1: h[1,i] = 1
                new_strat += 1
                s.append('{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100)))
                s_ref.append(h[:,i])

    return h, new_strat

def update_4(h,strat,av,s,s_ref,p_mut=None,change=None):
                                              #assign a probability to be killed and to be reproduced to every strategy based on 
    if p_mut == None: p_mut = 0               #its score
    if change == None: change = 1
    
    h = np.array(h)
    new_strat = 0
    
    dim = len(av)+1
    b=1/np.sum(np.arange(dim))
    prob_vec=[b]
   
    for i in range(2,dim):
        prob_vec.append(prob_vec[i-2]+(i)*b)
    prob_vec_1 = np.flip(np.array(prob_vec))          #builds the vector of the probabilities to be killed of each strategy
    
    if np.shape(h) == (len(h.T),): #NO mutation
        for i in range(change):
            if len(strat)<=1:break
            else:
                if len(strat)<3: 
                    w1=0
                    w2=-1
                else:
                    x1,x2 = npr.random(),npr.random()
                    
                    correct = len(prob_vec_1) -1         #need to check the list backward
                    for j in range(correct+1):           #selects the strategy to kill based on probabilities
                        if x1 <= prob_vec_1[correct-j]:
                            w1 = correct-j
                            break
                            
                    dim = len(av)-w1
                    b=1/np.sum(np.arange(dim))
                    prob_vec_2=[b]
                    for j in range(2,dim):
                        prob_vec_2.append(prob_vec_2[j-2]+(j)*b)   #builds the vector of the probabilities to reproduce of each 
                                                                   #strategy, among the strategies with a better score
                    
                    for j in range(len(prob_vec_2)):
                        if x2 <= prob_vec_2[j]:                    #selects the strategy that is going to reproduce
                            w2 = j + w1 +1
                            break
                        
                    if w2 == len(av): w2-=1
                            
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k=np.where(h==strat[w1])[0]
                    if len(k)<1:break
                    elif len(strat) == 1: break
                    else:h[k[0]]=strat[w2]
    
    else:                       #YES mutation
        for i in range(change):
            if len(strat.T)<=1: break
            else:
                if len(strat.T)<3: 
                    w1=0
                    w2=-1
                else: 
                    x1,x2 = npr.random(),npr.random()
                    
                    correct = len(prob_vec_1) -1         #need to check the list backward
                    for j in range(correct+1):           #selects the strategy to kill based on probabilities
                        if x1 <= prob_vec_1[correct-j]:
                            w1 = correct-j
                            break
                            
                    dim = len(av)-w1
                    b=1/np.sum(np.arange(dim))
                    prob_vec_2=[b]
                    for j in range(2,dim):
                        prob_vec_2.append(prob_vec_2[j-2]+(j)*b)   #builds the vector of the probabilities to reproduce of each 
                                                                   #strategy, among the strategies with a better score
                    for j in range(len(prob_vec_2)):
                        if x2 <= prob_vec_2[j]:                    #selects the strategy that is going to reproduce
                            w2 = j + w1 +1
                            break
                        
                    if w2 == len(av): w2-=1
                            
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
                h[1,i] = round(npr.random(),2)
                if h[1,i] > 1: h[1,i] = 1
                new_strat += 1
                s.append('{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100)))
                s_ref.append(h[:,i])

    return h, new_strat

def update_5(h,strat,av,s,s_ref,p_mut=None,change=None):
                                              #assign a probability to be killed and to be reproduced to every strategy based on 
    if p_mut == None: p_mut = 0               #its score
    if change == None: change = 1
    
    h = np.array(h)
    new_strat = 0
    
    uni = np.unique(av)
    
    if np.shape(h) == (len(h.T),): #NO mutation
        for i in range(change):
            if len(strat)<=1:break
            else:
                if len(uni) != 1:
                    w1,w2 = 0,-1
                    
                    prob_vec_inv = av[-1] - av
                    prob_vec_inv = prob_vec_inv/np.sum(prob_vec_inv)        #assign probabilities based on the % of the score
                    prob_vec_inv = np.flip(prob_vec_inv)
                    prob_vec1 = np.zeros(len(prob_vec_inv))
                    prob_vec1[0] = prob_vec_inv[0]                            #build the cumulative prob vector
                    for i in range(1,len(prob_vec_inv)):
                        prob_vec1[i]=prob_vec1[i-1]+prob_vec_inv[i]
                        
                    x1,x2 = npr.random(),npr.random()
                    
                    for j in range(len(prob_vec1)):           #selects the strategy to kill based on probabilities
                        if x1 < prob_vec1[j]:
                            w1 = len(prob_vec1)-1-j
                            break
                            
                    prob_vec = av[w1:]-av[w1]      #build the other probability vector
                    prob_vec = prob_vec/np.sum(prob_vec)
                    prob_vec2 = np.zeros(len(prob_vec))
                    prob_vec2[0] = prob_vec[0]    
                    for j in range(1,len(prob_vec)):
                        prob_vec2[j]=prob_vec[j]+prob_vec2[j-1]
                    
                    for j in range(len(prob_vec2)):
                        if x2 < prob_vec2[j]:                    #selects the strategy that is going to reproduce
                            w2 = j + w1
                            break
                     
                    if w2 == len(av): w2-=1
                else: break
                            
                if av[w1] != av[w2]:   #makes sure that I don't replace strategies with the same performance
                    k=np.where(h==strat[w1])[0]
                    if len(k)<1:break
                    elif len(strat) == 1: break
                    else:h[k[0]]=strat[w2]
    
    else:                       #YES mutation
        for i in range(change):
            if len(strat.T)<=1: break
            else:
                if len(uni) != 1: 
                    w1,w2 = 0,-1
                    
                    prob_vec_inv = av[-1] - av
                    prob_vec_inv = prob_vec_inv/np.sum(prob_vec_inv)        #assign probabilities based on the % of the score
                    prob_vec_inv = np.flip(prob_vec_inv)
                    prob_vec1 = np.zeros(len(prob_vec_inv))
                    prob_vec1[0] = prob_vec_inv[0]                            #build the cumulative prob vector
                    for i in range(1,len(prob_vec_inv)):
                        prob_vec1[i]=prob_vec1[i-1]+prob_vec_inv[i]
                        
                    x1,x2 = npr.random(),npr.random()
                    
                    for j in range(len(prob_vec1)):           #selects the strategy to kill based on probabilities
                        if x1 < prob_vec1[j]:
                            w1 = len(prob_vec1)-1-j
                            break
                            
                    prob_vec = av[w1:]-av[w1]      #build the other probability vector
                    prob_vec = prob_vec/np.sum(prob_vec)
                    prob_vec2 = np.zeros(len(prob_vec))
                    prob_vec2[0] = prob_vec[0]    
                    for j in range(1,len(prob_vec)):
                        prob_vec2[j]=prob_vec[j]+prob_vec2[j-1]
                    
                    for j in range(len(prob_vec2)):
                        if x2 < prob_vec2[j]:                    #selects the strategy that is going to reproduce
                            w2 = j + w1
                            break
                     
                    if w2 == len(av): w2-=1
                else: break
                            
                if av[w1] != av[w2]:        #makes sure that I don't replace strategies with the same performance
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
                h[1,i] = round(npr.random(),2)
                if h[1,i] > 1: h[1,i] = 1
                new_strat += 1
                s.append('{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100)))
                s_ref.append(h[:,i])

    return h, new_strat