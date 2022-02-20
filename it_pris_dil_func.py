from functools import partial
import strategies as st
import update_func as up
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_olivetti_faces
faces = fetch_olivetti_faces().images

strat = {'nice': partial(st.nice_guy),
        'bad': partial(st.bad_guy), 
        'm_nice': partial(st.mainly_nice),
        'm_bad': partial(st.mainly_bad),
        'tit_tat': partial(st.tit_tat),
        'random': partial(st.random),
        'grim': partial(st.grim),
        'f_tit_tat': partial(st.f_tit_tat),
        'sus_tit_tat': partial(st.sus_tit_tat),
        'pavlov': partial(st.pavlov),
        'reactive_nice': partial(st.reactive_nice),
        'reactive_bad': partial(st.reactive_bad),
        'hard_joss': partial(st.hard_joss),
        'soft_joss': partial(st.soft_joss)}

update = {'update_1': partial(up.update_1),
        'update_2': partial(up.update_2),
        'update_3': partial(up.update_3),
        'update_4': partial(up.update_4),
        'update_5': partial(up.update_5)}

def mutation(q, pq, i, w1, w2, w3):

    if npr.random() < pq:
        return strat['nice'](i,w1,w2,w3)
    else:
        return strat[q](i,w1,w2,w3)

def fight(f,g,probf=0,probg=0,N=None,graph=False, ):

    if N == None: N = 10
            
    R, S, T, P = 3, 0, 5, 1
    M = np.array([[R,S],[T,P]])

    p1, p2 = [-1,-1], [-1,-1]
    for i in range(2,N+2):
        if probf == 0 and probg == 0:
            p1.append(strat[f](i,p2[i-1],p1[i-1],p2[i-2]))
            p2.append(strat[g](i,p1[i-1],p2[i-1],p1[i-2]))
        else:
            p1.append(mutation(f,probf,i,p2[i-1],p1[i-1],p2[i-2]))
            p2.append(mutation(g,probg,i,p1[i-1],p2[i-1],p1[i-2]))

    p1 = np.array(p1[2:]).T
    p2 = np.array(p2[2:]).T

    result_1 = np.cumsum([np.dot(p1[:,i].T,np.dot(M,p2[:,i])) for i in range(N)])
    result_2 = np.cumsum([np.dot(p2[:,i].T,np.dot(M,p1[:,i])) for i in range(N)])

    if graph == True:
        plt.xlabel('iteration')
        plt.ylabel('points')
        plt.plot(result_1, label=f)
        plt.plot(result_2, label=g)
        plt.legend()
    
    return result_1[-1], result_2[-1]

def r_r(h,s):

    N = len(h)
    partecipants = [s[int(i)] for i in h] #h ma con i nomi

    result = np.zeros((N,N))
    somma = np.zeros(N)
    for i in range(N):
        for j in range(i+1,N):
            p1, p2 = fight(partecipants[i],partecipants[j])
            result[i,j] = p1
            result[j,i] = p2

        somma[i] = np.sum(result[i,:])

    unique, n_strategies = np.unique(h,return_counts=True)
    media = np.zeros(len(unique))

    for i in range(N):
        val = int(np.argwhere(unique == h[i]))
        media[val] += somma[i]

    media = np.round(media/n_strategies,2)

    return unique, media, n_strategies

def r_r_m(h,s):

    N = len(h.T)
    partecipants = [s[int(val)] for val in h[0]] #h ma con i nomi

    result = np.zeros((N,N))
    somma = np.zeros(N)
    for i in range(N):
        for j in range(i+1,N):
            p1, p2 = fight(partecipants[i],partecipants[j], probf=h[1,i], probg=h[1,j])
            result[i,j] = p1
            result[j,i] = p2

        somma[i] = np.sum(result[i,:])

    unique, n_strategies = np.unique(h,return_counts=True, axis=1)
    media = np.zeros(len(unique.T))
    for i in range(N):
        for j in range(len(unique.T)):
            if np.all(h[:,i] == unique[:,j]):
                val = j
        media[val] += somma[i]

    media = np.round(media/n_strategies,2)

    return unique, media, n_strategies

def round_robin(h,s,ord=False):

    h = np.array(h)

    if np.shape(h) == (len(h.T),): 
        u,m,n = r_r(h,s)
        if ord == True:
            sort = m.argsort()
            m = m[sort]
            u = u[sort]
            n = n[sort]
    else: 
        u,m,n = r_r_m(h,s)
        if ord == True:
            sort = m.argsort()
            m = m[sort]
            n = n[sort]
            u[0] = u[0,sort]    #sort first row
            u[1] = u[1,sort]    #sort second row
    return u, m, n

def tournament(h,f,s,it=None,mutation_prob=None,n_change=None):
    
    if it == None: it = 100
    s_ref = [[i,0] for i in range(len(s))]

    new_strat = 0
    n_matrix = np.zeros([it,len(s)])  #matrice per salvare il numero di strat per it
    val_matrix = np.zeros([it,len(s)])  #matrice per salvare il punteggio medio di una strat per it
    new_col = np.zeros((it,1))

    for i in range(it):    
        strategies, average_results, numbers = round_robin(h,s,ord=True)
        for j in range(new_strat):
            n_matrix = np.hstack((n_matrix,new_col))
            val_matrix = np.hstack((val_matrix,new_col))

        numbers_1 = np.zeros(len(n_matrix.T))
        average_1 = np.zeros(len(n_matrix.T))

        if np.shape(h) == (len(h.T),):   #NO mutations
            for j in range(len(strategies)):
                numbers_1[strategies[j]] = int(numbers[j])
                average_1[strategies[j]] = average_results[j]

        else:
            for j in range(len(strategies.T)):   #YES mutations
                for k in range(len(s_ref)):
                    if np.all(s_ref[k] == strategies[:,j]):
                        ind = k
                numbers_1[ind] = int(numbers[j])
                average_1[ind] = average_results[j]

        n_matrix[i] = numbers_1
        val_matrix[i] = average_1

        h, new_strat = update[f](h,strategies,average_results,s,s_ref,mutation_prob,n_change)

    return n_matrix, val_matrix