import random
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



def plot(solution, machines, jobs, path, img_filename=None, show=False, show_task_labels=True):
    colors = [ [ random.random() for i in range(3) ] for x in range(len(machines)) ]
    color_map = { R : colors[c] for c, R in enumerate(machines)}
    fig, ax = plt.subplots(1, 1, figsize=(15,5))
    resource_size = 1.0
    R_ticks = list()
    resource_height=1.0
    for j in jobs:
        R_ticks += [str(j)]*int(resource_size)
    for (T,R,x,x_) in solution :
        y = (jobs.index(T))*resource_height
        #print(x,y)
        ax.add_patch(patches.Rectangle((x, y),max(x_-x,0.5),resource_height,
                                       color = color_map[R],alpha=1))
        if show_task_labels :
            plt.text(x+0.4*max(x_-x,0.5),y+0.3*resource_height,str(machines.index(R)+1),fontsize=14,color='black')
    
    plt.title(str('Job shop'))
    plt.yticks([ resource_height*x + resource_height/2.0 for x in range(len(R_ticks)) ],R_ticks[::-1])
    plt.ylim(0,len(machines)*resource_height)#resource_height*len(resources))
    plt.xlim(0,max([ x_ for (I,R,x,x_) in solution]))
    plt.legend(handles=[mpatches.Patch(color=color_map[R], label=R) for R in machines],
               bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    

    if show:
        plt.show()
    #plt.grid(True)
    else:
        if img_filename:
            plt.savefig(path+img_filename, bbox_inches='tight')
        else:
            plt.savefig(path+'job_shop.pdf', bbox_inches='tight')
        plt.close()

        
def plot_2(solution, machines, jobs, path, show_task_labels=True):
    colors = [ [ random.random() for i in range(3) ] for x in range(len(machines)) ]
    color_map = { R : colors[c] for c, R in enumerate(machines)}
    fig, ax = plt.subplots(1, 1, figsize=(15,5))
    resource_size = 1.0
    R_ticks = list()
    resource_height=1.0
    for j in jobs:
        R_ticks += [str(j)]*int(resource_size)
    for (T,R,x,x_) in solution :
        y = (jobs.index(T))*resource_height
        #print(x,y)
        ax.add_patch(patches.Rectangle((x, y),max(x_-x,0.5),resource_height,
                                       color = color_map[R],alpha=1))
        if show_task_labels :
            plt.text(x+0.4*max(x_-x,0.5),y+0.3*resource_height,str(machines.index(R)+1),fontsize=14,color='black')
    
    plt.title(str('Job shop'))
    plt.yticks([ resource_height*x + resource_height/2.0 for x in range(len(R_ticks)) ],R_ticks[::-1])
    plt.ylim(0,len(machines)*resource_height)#resource_height*len(resources))
    plt.xlim(0,max([ x_ for (I,R,x,x_) in solution]))
    plt.legend(handles=[mpatches.Patch(color=color_map[R], label=R) for R in machines],
               bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    return fig