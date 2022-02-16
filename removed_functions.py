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
