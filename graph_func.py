#Graph_functions

import matplotlib.pyplot as plt
import seaborn as sns
import imageio as io
import os
import numpy as np

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
        plt.figure(figsize=(8,6.5))
        plt.barh(x[index], y, color=x_colors[index])
        plt.xlim(0,np.max(population)+3)
        plt.xlabel('Population', fontsize=15)
        plt.title('Population growth',fontsize=18)
        plt.text(np.max(population)-10, 0.1, f'iteration{index}',fontsize=15)

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