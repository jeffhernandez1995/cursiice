import xlwings as xw
from pulp import *
import pandas as pd
import numpy as np
import os
from pulp_extensions.solvers import Kestrel
from pulp_extensions.utils import plot_2


def job_shop():
    path=os.getcwd()
    path+='/'
    path="G:/Curso_iice/myproject/"
    
    #wb = xw.Book(os.path.abspath(path+'myproject.xlsm')) 
    wb = xw.Book.caller()
    sht_1 = wb.sheets['Times']
    sht_2 = wb.sheets['Precedencia']
    df_job = sht_1.range('A1').options(pd.DataFrame, expand='table').value
    (n_maq, n_trab)= df_job.shape
    df_pred= sht_2.range('A1').options(pd.DataFrame, expand='table').value
    
    jobs=['job'+str(i+1) for i in range(n_trab)]
    machines=['maq'+str(i+1) for i in range(n_maq)]
    stages=['pred'+str(i+1) for i in range(n_maq)]
    i_1=[]
    for j in jobs:
    	for t in stages:
    		if stages.index(t)+1>1:
    			for k in machines:
    				for m in machines:
    					k_=machines.index(k)+1
    					m_=machines.index(m)+1
    					if k_==df_pred['pred'+str(stages.index(t))][j] and m_==df_pred[t][j]:
    						i_1.append((j,k,m))
    
    i_2=[]
    for k in machines:
    	for j in jobs:
    		for i in jobs:
    			if jobs.index(j)<jobs.index(i):
    				i_2.append((j,i,k))
    
    
    prob = LpProblem("Job shop",LpMinimize)
    
    x=LpVariable.dicts('start_time', (jobs,machines),0,None,LpContinuous)
    y=LpVariable.dicts('precedencia', (jobs,jobs,machines) ,0,1,LpInteger)
    z=LpVariable('Objetivo',0,None,LpContinuous)
    
    prob += z
    for (j,k,m) in i_1:
    	prob += x[j][m]>= x[j][k]+df_job[k][j]
    
    for (j,i,k) in i_2:
    	prob += x[j][k]>= x[i][k]+df_job[k][i]-9999*y[j][i][k]
    	prob += x[i][k]>= x[j][k]+df_job[k][j]-9999*(1-y[j][i][k])
    
    for j in jobs:
    	for k in machines:
    		prob +=z>=x[j][k]+df_job[k][j]
    
    prob.solve(Kestrel(ptype='milp'))
    
    solution=[]
    for v in prob.variables():
        if v.name!='Objetivo':
            line=v.name.split(sep='_')
            if line[0]!='precedencia':
                solution.append((line[2], line[3], v.varValue, v.varValue+df_job[line[3]][line[2]]))
    solution=sorted(solution, key=lambda x : x[2])
    fig=plot_2(solution, machines, jobs, path)
    sht_3 = wb.sheets['Sheet1']
    sht_3.pictures.add(fig, name='job_shop', update=True)
