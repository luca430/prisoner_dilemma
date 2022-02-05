from functools import partial
import strategies as st
import update_func as up
import numpy as np
import matplotlib.pyplot as plt

strat = {'nice': partial(st.nice_guy),
        'bad': partial(st.bad_guy), 
        'm_nice': partial(st.mainly_nice),
        'm_bad': partial(st.mainly_bad),
        'tit_tat': partial(st.tit_tat)}

update = {'update_1': partial(up.update_1),
        'update_1rand': partial(up.update_1rand),
        'update_2': partial(up.update_2)}

def fight(f,g,N=None,graph=False):

    if N == None: N = 100
            
    R, S, T, P = 3, 0, 5, 1
    M = np.array([[R,S],[T,P]])

    p1, p2 = [-1], [-1]
    for i in range(1,N+1):
        p1.append(strat[f](i,p2[i-1]))
        p2.append(strat[g](i,p1[i-1]))

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

def round_robin(h,s,ord=False):
    N = len(h)
    partecipants = [s[i] for i in h] #h ma con i nomi

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

    media = media/n_strategies
    
    if ord == True:
        sort = media.argsort()
        media = media[sort]
        unique = unique[sort]

    return unique, media

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