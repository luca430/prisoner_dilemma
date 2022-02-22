from functools import partial
import strategies as st
import update_func as up
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

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

def mutation(player,gene,it,u,v,u2):

    if npr.random() < gene:
        return [1,0]
    else:
        return strat[player](it,u,v,u2)


def fight(player1,player2,prob1=0,prob2=0,N=None,graph=False,all_outcome=False):


    if N == None: N = 100
            
    R, S, T, P = 3, 0, 5, 1
    M = np.array([[R,S],[T,P]])

    p1, p2 = [-1,-1], [-1,-1]
    for i in range(2,N+2):
        if prob1 == 0 and prob2 == 0:   #NO mutation 
            p1.append(strat[player1](i,p2[i-1],p1[i-1],p2[i-2]))
            p2.append(strat[player2](i,p1[i-1],p2[i-1],p1[i-2]))
        else:                           #YES mutation
            p1.append(mutation(player1,prob1,i,p2[i-1],p1[i-1],p2[i-2]))
            p2.append(mutation(player2,prob2,i,p1[i-1],p2[i-1],p1[i-2]))

    p1 = np.array(p1[2:]).T
    p2 = np.array(p2[2:]).T

    result_1 = np.cumsum([np.dot(p1[:,i].T,np.dot(M,p2[:,i])) for i in range(N)])
    result_2 = np.cumsum([np.dot(p2[:,i].T,np.dot(M,p1[:,i])) for i in range(N)])

    if graph == True:
        ax = plt.figure().gca()
        plt.xlabel('iteration')
        plt.ylabel('points')
        plt.plot(result_1, label=player1)
        plt.plot(result_2, label=player2)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend()


    if all_outcome == False:    #print only the final results
        return result_1[-1], result_2[-1]

    else:                       #also print all uc and ud vectors (useful for fight_grid)
        return result_1[-1], result_2[-1], [player1,p1], [player2,p2]

def r_r(h,s):

    N = len(h)
    partecipants = [s[int(i)] for i in h]   #h but with strings

    result = np.zeros((N,N))
    score = np.zeros(N)

    for i in range(N):
        for j in range(i+1,N):      #avoid the fights along the diagonal
            p1, p2 = fight(partecipants[i],partecipants[j])
            result[i,j] = p1
            result[j,i] = p2

        score[i] = np.sum(result[i,:])  #final score of i-th player

    unique, n_strategies = np.unique(h,return_counts=True)
    mean = np.zeros(len(unique))

    for i in range(N):
        idx = int(np.argwhere(unique == h[i]))      #build mean with the same sorting of unique
        mean[idx] += score[i]

    mean = np.round(mean/n_strategies,2)

    return unique, mean, n_strategies

def r_r_m(h,s):        #adaptation of r_r for the mutation case

    N = len(h.T)
    partecipants = [s[int(val)] for val in h[0]]

    result = np.zeros((N,N))
    score = np.zeros(N)
    for i in range(N):
        for j in range(i+1,N):
            p1, p2 = fight(partecipants[i],partecipants[j], prob1=h[1,i], prob2=h[1,j])
            result[i,j] = p1
            result[j,i] = p2

        score[i] = np.sum(result[i,:])

    unique, n_strategies = np.unique(h,return_counts=True, axis=1)
    mean = np.zeros(len(unique.T))
    for i in range(N):                              #adaptation of argwhere() for bidimensional case
        for j in range(len(unique.T)):
            if np.all(h[:,i] == unique[:,j]):
                idx = j
        mean[idx] += score[i]

    mean = np.round(mean/n_strategies,2)

    return unique, mean, n_strategies

def round_robin(h,s,ord=False):

    h = np.array(h)

    if np.shape(h) == (len(h.T),): 
        u,m,n = r_r(h,s)
        if ord == True:
            sort = m.argsort()      #create a mask that orders m,u,n from the lowest score to the higher
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

def tournament(h,update_f,s,it=None,mutation_prob=None,n_change=None):

    h = np.array(h)
 
    if it == None: it = 100
    s_ref = [[i,0] for i in range(len(s))]  #associate a list [index,mut=0] for each strategy in s

    if np.shape(h) != (len(h.T),):
        for i in range(len(h[1])):          #check if a mutation is already present at the beginning and initialize it
            if h[1,i] != 0:
                check=0
                string = '{}_{}'.format(s[int(h[0,i])],int(h[1,i]*100))
                for val in s:
                    if val == string:
                        check = 1
                if check == 0:
                    s_ref.append(h[:,i])
                    s.append(string)

    new_strat = 0
    n_matrix = np.zeros([it,len(s)])                   #matrix of the number of strategies at each iteration
    val_matrix = np.zeros([it,len(s)])                 #matrix of the average scores at each iteration
    new_col = np.zeros((it,1))
    count = 0
    for i in range(it):    
        strategies, average_results, numbers = round_robin(h,s,ord=True)
        
        for j in range(new_strat):                     #adds a new column to n_matrix and val_matrix 
            n_matrix = np.hstack((n_matrix,new_col))   #for each new strategy born in the previous iteration
            val_matrix = np.hstack((val_matrix,new_col))

        numbers_1 = np.zeros(len(n_matrix.T))
        average_1 = np.zeros(len(n_matrix.T))

        if np.shape(h) == (len(h.T),):                 #NO mutations
            for j in range(len(strategies)):
                numbers_1[strategies[j]] = int(numbers[j])
                average_1[strategies[j]] = average_results[j]

        else:
            for j in range(len(strategies.T)):         #YES mutations
                for k in range(len(s_ref)):            #new slicing method adapted for 2-dim h
                    if np.all(s_ref[k] == strategies[:,j]):
                        ind = k
                numbers_1[ind] = int(numbers[j])
                average_1[ind] = average_results[j]

        n_matrix[i] = numbers_1
        val_matrix[i] = average_1
        
        if len(np.unique(average_results)) == 1:        #break at convergence
            count+=1
            if count == 1: tresh = i
            if count == int(tresh/10) + 3:
                break

        h, new_strat = update[update_f](h,strategies,average_results,s,s_ref,mutation_prob,n_change)

    n_matrix1 = np.copy(n_matrix[:i,:])
    val_matrix1 = np.copy(val_matrix[:i,:])
    return n_matrix1, val_matrix1, i

def h_build(numbers,mutation = False):
    if mutation == False:
        h = []
        for i in range(len(numbers)):
            for j in range(numbers[i]):
                h.append(i)
        return np.array(h)
    if mutation == True:
        h = np.zeros((2,np.sum(numbers)))
        h1 = []
        for i in range(len(numbers)):
            for j in range(numbers[i]):
                h1.append(i)
        h[0] = h1
        return np.array(h)
