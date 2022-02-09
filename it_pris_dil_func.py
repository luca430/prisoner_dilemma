from functools import partial
import strategies as st
import update_func as up
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt

strat = {'nice': partial(st.nice_guy),
        'bad': partial(st.bad_guy), 
        'm_nice': partial(st.mainly_nice),
        'm_bad': partial(st.mainly_bad),
        'tit_tat': partial(st.tit_tat)}

update = {'update_1': partial(up.update_1),
        'update_1rand': partial(up.update_1rand),
        'update_2': partial(up.update_2)}

def mutation(q, pq, i, w):

    if npr.random() < pq:
        return strat['nice'](i,w)
    else:
        return strat[q](i,w)

def fight(f,g,probf=0,probg=0,N=None,graph=False):

    if N == None: N = 100
            
    R, S, T, P = 3, 0, 5, 1
    M = np.array([[R,S],[T,P]])

    p1, p2 = [-1], [-1]
    for i in range(1,N+1):
        if probf == 0 and probg == 0:
            p1.append(strat[f](i,p2[i-1]))
            p2.append(strat[g](i,p1[i-1]))
        else:
            p1.append(mutation(f,probf,i,p2[i-1]))
            p2.append(mutation(g,probg,i,p1[i-1]))

    p1 = np.array(p1[1:]).T
    p2 = np.array(p2[1:]).T

    result_1 = np.cumsum([np.dot(p1[:,i].T,np.dot(M,p2[:,i])) for i in range(N)])
    result_2 = np.cumsum([np.dot(p2[:,i].T,np.dot(M,p1[:,i])) for i in range(N)])

    if graph == True:
        plt.xlabel('iteration')
        plt.ylabel('points')
        plt.plot(result_1, label=f)
        plt.plot(result_2, label=g)
        plt.legend()

    return [result_1[-1], result_2[-1]]


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

    return unique, media

def r_r_m(h,s):

    N = len(h.T)
    partecipants = [s[int(i)] for i in h[0]] #h ma con i nomi

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

    return unique, media

def round_robin(h,s,ord=False):

    h = np.array(h)

    if np.shape(h) == (len(h.T),): 
        u,m = r_r(h,s)
        if ord == True:
            sort = m.argsort()
            m = m[sort]
            u = u[sort]
    else: 
        u,m = r_r_m(h,s)
        if ord == True:
            sort = m.argsort()
            m = m[sort]
            u = u.T
            u = u[sort]
            u = u.T

    return u, m


def tournament(h,f,s,it=None):
    
    if it == None: it = 100

    n_matrix = np.zeros([it,len(s)])  #matrice per salvare il numero di strat per it
    val_matrix = np.zeros([it,len(s)])  #matrice per salvare il punteggio medio di una strat per it
    
    for i in range(it):
        strategies, average_results = round_robin(h,s)
        unique, numbers = np.unique(h, return_counts = True)
        numbers_1 = np.array([0 for i in range(len(s))])
        average_1 = np.array([0 for i in range(len(s))])

        for j in range(len(unique)):
            numbers_1[unique[j]] = int(numbers[j])
            average_1[strategies[j]] = average_results[j]

        n_matrix[i] = numbers_1
        val_matrix[i] = average_1

        h = update[f](h,strategies,average_results)

    return n_matrix, val_matrix