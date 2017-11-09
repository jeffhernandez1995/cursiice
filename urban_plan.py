from pulp import *
#from openpyxl import load_workbook
import pandas as pd

n_proy=4
n_años=5
proyectos=['Proyecto '+str(i) for i in range(1,n_proy+1)]
años=['Año '+str(i) for i in range(1, n_años+1)]



xl=pd.ExcelFile('/home/jeff/grive/Investigación_de_operaciones/Curso_iice/data.xlsx')
df = xl.parse("Hoja1")


prob = LpProblem("urban planning",LpMaximize)

comb=[(p, a) for p in proyectos for a in años]
vars = LpVariable.dicts("comb",(proyectos,años),0,1,LpContinuous)

prob+=lpSum([df['Ingreso'][p]*(5-int(a[4]))*df[a][p]*vars[p][a] for (p,a) in comb])
prob+=lpSum([vars['Proyecto 1'][a] for a in años])==1
prob+=lpSum([vars['Proyecto 4'][a] for a in años])==1
prob+=lpSum([vars['Proyecto 2'][a] for a in años])>=0.25
prob+=lpSum([vars['Proyecto 2'][a] for a in años])<=1
prob+=lpSum([vars['Proyecto 3'][a] for a in años])>=0.25
prob+=lpSum([vars['Proyecto 3'][a] for a in años])<=1
for a in años:
    prob+=lpSum([vars[p][a]*df['Costo'][p] for p in proyectos])<=df[a]['Presupuesto']

prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total earnings = ", value(prob.objective))