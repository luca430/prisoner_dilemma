def plot_bar_graph():
fig, ax = plt.subplots(figsize=(7.5,5))

col=[i for i in sns.color_palette("flare",n_colors=len(s)) ]  
font = {'family': 'monospace',
        'color':  'black',
        'weight': 'medium'}

def autolabel(rects):
    for idx,rect in enumerate(plot_bar):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.,
                0.5*height, media[idx], ha='center',
                va='center', rotation=0, fontdict=font)
        
plot_bar=plt.bar(s_unique,media,color=col,width=0.8)
autolabel(plot_bar)


punto 4
fig4, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(15,5))

val_ma_graph = np.copy(val_ma4)

val_ma_graph[val_ma_graph == 0] = np.nan

for i in range(len(n_ma4.T)):
    k=np.where(val_ma4.T[i]==0)[0]
    if len(k)>0:
        if k.max()==iterations-1: #caso morti prima
            position_1=[k[y]-1 for y in range(1,len(k)) if k[y-1]+1!=k[y]]
            if k.min()!=0:
                ax2.plot(np.arange(iterations)[k.min()-1],
                         val_ma_graph.T[i,k.min()-1],'x',color='red',
                         markeredgewidth=2)#caso nati all'inizio 
            if len(position_1)>0:
                ax2.plot(np.arange(iterations)[position_1],val_ma_graph.T[i,position_1],
                         'x',color='red',markeredgewidth=2) #caso nasce dopo   
        if k.min()==0: #caso nati dopo
            position_2=[y+1 for y in range(len(k)-1) if k[y]+1!=k[y+1]] 
            position_3=[w+1 for w in range(len(k)) if k.max()!=iterations-1]
            if len(position_2)>0:
                ax2.plot(position_2,val_ma_graph.T[i,position_2],'o',color='green')#caso morti 
            if len(position_3)>0:
                ax2.plot(max(position_3),val_ma_graph.T[i,max(position_3)],'o',color='green')#caso non morti

    ax2.plot(0,val_ma_graph.T[i,0],'o',color='green')    #caso nati all'inizio non morti 
    ax2.plot(np.arange(iterations)[-1],val_ma_graph.T[i,-1],'x',color='red',markeredgewidth=2)#caso nati all'inizio non morti
    ax1.plot(np.arange(iterations),n_ma4.T[i])
    ax2.plot(np.arange(iterations),val_ma_graph.T[i],label=s[i])



ax2.set_title('Average points')
ax1.set_title('Population')
fig4.legend(loc='center right')
plt.show()

fig4_1,ax4_1=plt.subplots(figsize=(15,8))
ax4_1.stackplot(np.arange(iterations),n_ma4.T,labels=s,alpha=0.9);
fig4_1.legend(loc='center right')
plt.xlim(range(iterations)[0],range(iterations)[-1])
ax4_1.set_title('Population') 
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)
plt.show()


33
s = ['nice','bad','m_nice','m_bad','tit_tat']#,'random','pavlov','f_tit_tat']

h = npr.randint(0,len(s),size=10)
unique, n_strategies = np.unique(h,return_counts=True)

for a,b in zip(unique,n_strategies): print(s[a],b)

iterations = 20
n_ma3, val_ma3 = pris_dil.tournament(h,'update_2',s,it=iterations)

val_ma_graph = np.copy(val_ma3)
val_ma_graph[val_ma_graph == 0] = np.nan

s_colors = ['lime','red','cyan','saddlebrown','darkslategray','olive',
            'purple','navy','darkviolet','gold','darkgreen','darkorange',
            'royalblue','hotpink']


fig3, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(15,5))
for i in range(len(s)):
    ax2.plot(0,val_ma_graph.T[i,0],'o',color='green')
    for j in range(len(val_ma_graph.T[i])):
        if np.isnan(val_ma_graph.T[i,j])==True: 
            ax2.plot(np.arange(iterations)[j-1],val_ma_graph.T[i,j-1],'x',color='red',markeredgewidth=2)
    ax1.plot(np.arange(iterations),n_ma3.T[i],color=s_colors[i])
    ax2.plot(np.arange(iterations),val_ma_graph.T[i],label=s[i],color=s_colors[i])


ax1.set_title('Population') 
ax2.set_title('Average points')
fig3.legend(loc='center right')
plt.show()

fig3_1,ax3_1=plt.subplots(figsize=(15,5))
ax3_1.stackplot(np.arange(iterations),n_ma3.T,labels=s,alpha=0.9);
fig3_1.legend(loc='center right')
plt.xlim(range(iterations)[0],range(iterations)[-1])
ax3_1.set_title('Population') 
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)
plt.show()

2 
fig, ax = plt.subplots(figsize=(7.5,5))

col=[i for i in sns.color_palette("flare",n_colors=len(s)) ]  
font = {'family': 'monospace',
        'color':  'black',
        'weight': 'medium'}

def autolabel(rects):
    for idx,rect in enumerate(plot_bar):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.,
                0.5*height, media[idx], ha='center',
                va='center', rotation=0, fontdict=font)
        
plot_bar=plt.bar(s_unique,media,color=col,width=0.8)
autolabel(plot_bar)