#Graph_functions

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import imageio as io
import os

def gif(s,population,file_name,colors):
    x = []
    x_colors = []
    coordinates_lists = np.zeros((len(population),len(s)))
    s = np.array(s)
    colors = np.array(colors)
    for i in range(len(population)):
        sort = population[i].argsort()
        x.append(s[sort])
        x_colors.append(colors[sort])
        coordinates_lists[i] = population[i,sort]
        
    filenames = []
    for index, y in enumerate(coordinates_lists):
        # plot charts
        plt.figure(figsize=(11,9.5))
        plt.barh(x[index], y, color=x_colors[index])
        plt.xlim(0,np.max(population)*(1+1/7))
        plt.xlabel('Population', fontsize=15)
        plt.title('Population growth',fontsize=18)
        plt.text(np.max(population), 0.1, f'iteration{index}',fontsize=12)

        for i, v in enumerate(y):
            if int(v) == 0: plt.text(v + 0.5 , i, str(int(v)), color='red', fontweight='bold')
            else:   plt.text(v + 0.5, i, str(int(v)), fontweight='bold')
        
        # create file name and append it to a list
        filename = f'{index}.png'
        for i in range(2): filenames.append(filename) #stack the same file more then once to slow down the animation
        
        # repeat last frame
        if (index == 0):
            for i in range(15):
                filenames.append(filename)

        if (index == len(coordinates_lists)-1):
            for i in range(15):
                filenames.append(filename)
                
        # save frame
        plt.savefig(filename)
        plt.close()
    # build gif
    with io.get_writer(f'{file_name}.gif', mode='I') as writer:
        for filename in filenames:
            image = io.imread(filename)
            writer.append_data(image)
            
    # Remove files
    for filename in set(filenames):
        os.remove(filename)
    return

def graph_bar(media,unique,s,col):
    
    col_1=[col[val] for val in unique]
    
    #col=[i for i in sns.color_palette("flare",n_colors=len(s_unique)) ] 
    
    def autolabel(rects):
        for idx,rect in enumerate(plot_bar):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2.,
                    0.5*height, media[idx], ha='center',
                    va='center', rotation=0, fontdict=font)
    
    fig, ax = plt.subplots(figsize=(15.5,7))
    font = {'family': 'sans',
            'color':  'black',
            'weight': 'heavy',
            'fontsize': 11}
    s_unique = [s[val] for val in unique]   
    plot_bar=ax.bar(s_unique,media,color=col_1,width=0.8)
    ax.set_title('Average points',fontsize=20)
    
    return autolabel(plot_bar)

def graph_avarege(h,s_colors,val_ma,s,iterations):
    
    val_ma_graph = np.copy(val_ma)
    val_ma_graph[val_ma_graph == 0] = np.nan
    
    fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(15,8.5))
    
    if np.shape(h) == (len(h.T),): #caso senza mutazione
        for i in range(len(s)):
            ax.plot(0,val_ma_graph.T[i,0],'o',color='green')
            ax.plot(np.arange(iterations)[-1],val_ma_graph.T[i,-1],'x',color='red',markeredgewidth=2)
            for j in range(len(val_ma_graph.T[i])):
                if np.isnan(val_ma_graph.T[i,j])==True: 
                    ax.plot(np.arange(iterations)[j-1],val_ma_graph.T[i,j-1],'x',color='red',markeredgewidth=2)
            ax.plot(np.arange(iterations),val_ma_graph.T[i],label=s[i],color=s_colors[i])
        ax.set_title('Average points without mutation strategies',fontsize=14)
    else:#caso mutazioni
        for i in range(len(val_ma.T)):
            k=np.where(val_ma.T[i]==0)[0]
            if len(k)>0:
                if k.max()==iterations-1: #caso morti prima
                    position_1=[k[y]-1 for y in range(1,len(k)) if k[y-1]+1!=k[y]]
                    if k.min()!=0:
                        ax.plot(np.arange(iterations)[k.min()-1],
                                 val_ma_graph.T[i,k.min()-1],'x',color='red',
                                 markeredgewidth=2)#caso nati all'inizio 
                    if len(position_1)>0:
                        ax.plot(np.arange(iterations)[position_1],
                                 val_ma_graph.T[i,position_1],
                                 'x',color='red',markeredgewidth=2) #caso nasce dopo   
                if k.min()==0: #caso nati dopo
                    position_2=[y+1 for y in range(len(k)-1) if k[y]+1!=k[y+1]] 
                    position_3=[w+1 for w in range(len(k)) if k.max()!=iterations-1]
                    if len(position_2)>0:
                        ax.plot(position_2,
                                 val_ma_graph.T[i,position_2],'o',color='green')#caso morti 
                    if len(position_3)>0:
                        ax.plot(max(position_3),
                                 val_ma_graph.T[i,max(position_3)],
                                 'o',color='green')#caso non morti

            ax.plot(0,val_ma_graph.T[i,0],'o',color='green')    #caso nati all'inizio non morti 
            ax.plot(np.arange(iterations)[-1],
                     val_ma_graph.T[i,-1],'x',color='red',markeredgewidth=2)#caso nati all'inizio non morti
            ax.plot(np.arange(iterations),
                     val_ma_graph.T[i],label=s[i],color=s_colors[i])
        ax.set_title('Average points mutation strategies',fontsize=14)
    
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Average points')
    fig.legend(loc='center right')
    plt.show()
    return
    
def graph_population(n_ma,iterations,s,s_colors):
    fig,ax=plt.subplots(figsize=(15,8.5))
    ax.stackplot(np.arange(iterations),n_ma.T,labels=s,alpha=0.9,colors=s_colors);
    fig.legend(loc='center right')
    plt.xlim(range(iterations)[0],range(iterations)[-1])
    ax.set_title('Population') 
    plt.gca().spines["top"].set_alpha(0)
    plt.gca().spines["bottom"].set_alpha(.3)
    plt.gca().spines["right"].set_alpha(0)
    plt.gca().spines["left"].set_alpha(.3)
    plt.show()
    return

def up_color(s,s_colors):
    s_mut = s[14:] #solo mutazioni di s
    for i in range(len(s_mut)):
        check_s_1 = s_mut[i][:-2]
        check_s_2 = s_mut[i][:-3]
        for j in range(len(s)):
            if s[j] == check_s_1:
                shade = [col for col in sns.light_palette(s_colors[j],n_colors=100,reverse=True)]
                s_2 = [l for l in s_mut[i]]
                s_colors.append(shade[int(s_2[-1])])
            if s[j] == check_s_2:
                shade = [col for col in sns.light_palette(s_colors[j],n_colors=100,reverse=True)]
                s_2 = [l for l in s_mut[i]]
                s_colors.append(shade[int(s_2[-2] + s_2[-1])])
    return s_colors