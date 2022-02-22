#Graph_functions

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import imageio as io
import os
from matplotlib import colors
from matplotlib.ticker import AutoMinorLocator

s_colors = {'nice': 'lime',
        'bad': 'red', 
        'm_nice': 'cyan',
        'm_bad': 'saddlebrown',
        'tit_tat': 'darkslategray',
        'random': 'olive',
        'grim': 'crimson',
        'f_tit_tat': 'navy',
        'sus_tit_tat': 'darkviolet',
        'pavlov': 'gold',
        'reactive_nice': 'darkgreen',
        'reactive_bad': 'darkorange',
        'hard_joss': 'royalblue',
        'soft_joss': 'hotpink'}

def up_color(s,start_s):
    
    colors = [s_colors[s[i]] for i in range(start_s)]
    s_mut = s[start_s:]                                 #only mutation of s
    for i in range(len(s_mut)):
        check_s_1 = s_mut[i][:-2]
        check_s_2 = s_mut[i][:-3]
        for j in range(len(s)):
            if s[j] == check_s_1:
                shade = [col for col in sns.light_palette(colors[j],n_colors=100,reverse=True)]
                s_2 = [l for l in s_mut[i]]
                colors.append(shade[int(s_2[-1])])
            if s[j] == check_s_2:
                shade = [col for col in sns.light_palette(colors[j],n_colors=100,reverse=True)]
                s_2 = [l for l in s_mut[i]]
                colors.append(shade[int(s_2[-2] + s_2[-1])])
    return colors

def gif(s,population,file_name,start_s=None):
    
    if start_s == None:
        colors = [s_colors[val] for val in s]
    else:
        colors = [s_colors[s[i]] for i in range(start_s)]
        colors = up_color(s,start_s)
        
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

def graph_bar(media,unique,n_unique,s):
    col = [s_colors[val] for val in s]
    col_1=[col[val] for val in unique]
    
    def autolabel(plot_bar,col_1):
        for idx,rect in enumerate(plot_bar):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2.,
                    1.01*height, media[idx], ha='center',
                    va='bottom', rotation=0, fontdict=font, color='black')
            
            if col_1[idx]=='navy' or col_1[idx]=='darkslategray' or col_1[idx]=='darkgreen' or col_1[idx]=='darkviolet':
                text_col = 'white'
            else: text_col = 'black'
            ax.text(rect.get_x() + rect.get_width()/2.,
                    0.5*height, n_unique[idx], ha='center',
                    va='center', rotation=0, fontdict=font, color=text_col)
    
    fig, ax = plt.subplots(figsize=(15.5,7))
    font = {'family': 'sans',
            'weight': 'heavy',
            'fontsize': 11}
    s_unique = [s[val] for val in unique]   
    plot_bar=ax.bar(s_unique,media,color=col_1,width=0.8)
    ax.set_ylim(0,np.max(media)*(1+1/5))
    ax.set_title('Average points',fontsize=20)
    
    return autolabel(plot_bar,col_1)

def graph_average(h,val_ma,s,iterations,start_s=None):

    h = np.array(h)

    if start_s == None:
        colors = [s_colors[val] for val in s]
    else:
        colors = [s_colors[s[i]] for i in range(start_s)]
        colors = up_color(s,start_s)
        
    val_ma_graph = np.copy(val_ma)
    val_ma_graph[val_ma_graph == 0] = np.nan
  
    fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(14,8.5))
    
    if np.shape(h) == (len(h.T),): #NO mutations
        for i in range(len(s)):
            ax.plot(0,val_ma_graph.T[i,0],'o',color='green')
            ax.plot(np.arange(iterations)[-1],val_ma_graph.T[i,-1],'x',color='red',markeredgewidth=2)
            for j in range(len(val_ma_graph.T[i])):
                if np.isnan(val_ma_graph.T[i,j])==True: 
                    ax.plot(np.arange(iterations)[j-1],val_ma_graph.T[i,j-1],'x',color='red',markeredgewidth=2)
            ax.plot(np.arange(iterations),val_ma_graph.T[i],label=s[i],color=colors[i])
        ax.set_title('Average points without mutation strategies',fontsize=14)
        
    else:  #YES mutations
        for i in range(len(val_ma.T)):
            k=np.where(val_ma.T[i]==0)[0]
            if len(k)>0:
                if k.max()==iterations-1:                                          #case previous death
                    position_1=[k[y]-1 for y in range(1,len(k)) if k[y-1]+1!=k[y]]
                    if k.min()!=0:
                        ax.plot(np.arange(iterations)[k.min()-1],
                                 val_ma_graph.T[i,k.min()-1],'x',color='red',
                                 markeredgewidth=2)                                #case born at the beginnig  
                    if len(position_1)>0:
                        ax.plot(np.arange(iterations)[position_1],
                                 val_ma_graph.T[i,position_1],
                                 'x',color='red',markeredgewidth=2)                #case born later   
                if k.min()==0:                                                     #caso born later
                    position_2=[y+1 for y in range(len(k)-1) if k[y]+1!=k[y+1]] 
                    position_3=[w+1 for w in range(len(k)) if k.max()!=iterations-1]
                    if len(position_2)>0:
                        ax.plot(position_2,
                                 val_ma_graph.T[i,position_2],'o',color='green')   #case death
                    if len(position_3)>0:
                        ax.plot(max(position_3),
                                 val_ma_graph.T[i,max(position_3)],
                                 'o',color='green')                                 #case not death

            ax.plot(0,val_ma_graph.T[i,0],'o',color='green')                #case born at the beginnig and death 
            ax.plot(np.arange(iterations)[-1],
                     val_ma_graph.T[i,-1],'x',color='red',markeredgewidth=2)#caso born at the beginnig and not death
            ax.plot(np.arange(iterations),
                     val_ma_graph.T[i],label=s[i],color=colors[i])
        ax.set_title('Average points mutation strategies',fontsize=14)
    
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Average points')
    plt.show()
    return
    
def graph_population(n_ma,s,iterations,start_s=None):
    
    if start_s == None:
        colors = [s_colors[val] for val in s]
    else:
        colors = [s_colors[s[i]] for i in range(start_s)]
        colors = up_color(s,start_s)
        
    #plot
    fig,ax=plt.subplots(figsize=(14,8.5))
    ax.stackplot(np.arange(iterations),n_ma.T,labels=s,alpha=0.9,colors=colors);
    plt.xlim(range(iterations)[0],range(iterations)[-1])
    
    #plot setup 
    ax.set_title('Population',fontsize=14)
    ax.set_xlabel('Iterations')
    plt.gca().spines["top"].set_alpha(0)
    plt.gca().spines["bottom"].set_alpha(.3)
    plt.gca().spines["right"].set_alpha(0)
    plt.gca().spines["left"].set_alpha(.3)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height])
    ax.legend(loc='center left',bbox_to_anchor=(1, 0.5),prop={'size':16})
    plt.show()
  
    return

def fight_grid(p1,p2,range=[None,None]):

    if range == [None,None]: range = [0,20]
    
    player1 = p1[0]                 
    player2 = p2[0]
    outcome1 = np.array(p1[1])
    outcome2 = np.array(p2[1])

    data = np.array([outcome1[0,range[0]:range[1]],outcome2[0,range[0]:range[1]]])
    # create discrete colormap
    cmap = colors.ListedColormap(['red', 'green'])
    bounds = [0,0.5,1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=(15,8))
    ax.imshow(data, cmap=cmap, norm=norm)

    # draw gridlines
    ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=1)
    ax.set_xlabel('iteration')
    ax.set_xticks(np.arange(0, range[1]-range[0], 1));
    ax.set_xticklabels(np.arange(range[0],range[1]));
    ax.set_yticks(np.arange(0, 2, 1));
    ax.set_yticklabels([player1,player2]);
    minor_locator = AutoMinorLocator(2)
    plt.gca().xaxis.set_minor_locator(minor_locator)
    minor_locator = AutoMinorLocator(2)
    plt.gca().yaxis.set_minor_locator(minor_locator)

    plt.show()
