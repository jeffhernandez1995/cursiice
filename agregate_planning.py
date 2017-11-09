from pulp import *
import pandas as pd

n_prod=7
n_maq=6
n_mes=4
n_per=9


maquinas=['Maquina '+str(i+1) for i in range(n_maq)]
meses=['Mes '+str(i+1) for i in range(n_mes+1)]
productos=['Producto '+str(i+1) for i in range(n_prod)]
periodos=['Periodo '+str(i) for i in range(n_per)]

xl=pd.ExcelFile('/home/jeff/grive/Investigación_de_operaciones/Curso_iice/dataframe_pa.xlsx')
dict_df={prod:xl.parse(prod) for prod in productos}
df_time=xl.parse("Tiempo")
df_disp=xl.parse("Disponibilidad")

prob = LpProblem("agregate planning",LpMinimize)

i_x=[(j,tau,t) for j in productos for tau in periodos for t in meses]
i_y=[(i,t) for i in maquinas for t in meses]
i_z=[(j,tau) for j in productos for tau in periodos]

x=LpVariable.dicts('Cantidad producida',(productos, periodos, meses),0,None,LpContinuous)
y=LpVariable.dicts('Numero', (maquinas, meses),0, None,LpInteger)
z=LpVariable.dicts('maq trabajando', (productos, periodos),0,1,LpInteger)

prob += lpSum([dict_df[j][t][tau]*x[j][tau][t] for (j,tau,t) in i_x])+lpSum(
	[df_disp['Costo_fijo2'][i]*y[i][t] for (i,t) in i_y])+lpSum(
	[dict_df['Producto 1']['Costo_fijo1'][tau]*z[j][tau] for (j,tau) in i_z])

for j in productos:
	for t in meses:
		prob += lpSum([x[j][tau][t] for tau in periodos])>=dict_df[j][t]['Demand']

for t in meses:
	for i in maquinas:
		prob+= lpSum([df_time[j][i]*x[j][tau][t] for (j,tau) in i_z])<=16*dict_df['Producto 1'][t]['Days']*y[i][t]
		prob+= y[i][t]<=df_disp[t][i]

for j in productos:
	for tau in periodos:
		prob += lpSum([x[j][tau][t] for t in meses])<=z[j][tau]*dict_df['Producto 1']['Capacity'][tau]


prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total cost= ", value(prob.objective))

