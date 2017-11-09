import numpy as np
from pulp_extensions.utils import plot
import os

path=os.getcwd()
path+='/'
path="G:/Curso_iice/"

solution=np.load(path+'solution.npz')['arr_0'][0]
temp=[]
for i in range(len(solution)):
    temp.append((solution[i][0], solution[i][1], float(solution[i][2]), float(solution[i][3])))

    
solution=temp
n_maq=10
n_trab=10
jobs=['job'+str(i+1) for i in range(n_trab)]
machines=['maq'+str(i+1) for i in range(n_maq)]
plot(solution, machines, jobs, path)