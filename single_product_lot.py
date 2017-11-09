from pulp import *


time=['1','2','3','4']

demand={'1':130,
        '2':80,
        '3':125,
        '4':195}

normal_cost={'1':6,
             '2':4,
             '3':8,
             '4':9}

over_cost={'1':8,
           '2':6,
           '3':10,
           '4':11}

over_cap={'1':60,
          '2':65,
          '3':70,
          '4':70}


prob = LpProblem("Production planning",LpMinimize)

x = LpVariable.dicts('normal_prod', time, 0, 100,LpContinuous)
y = LpVariable.dicts('over_prod', time,0,None, LpContinuous)
i = LpVariable.dicts('invetory', time, 0, 70, LpContinuous)


prob += lpSum([x[t]*normal_cost[t]+y[t]*over_cost[t]+1.5*i[t] for t in time])

for t in time:
    prob += y[t]<=over_cap[t]

prob += i['1']==15+x['1']+y['1']-demand['1']

for item, t in enumerate(time[1:]):
    prob += i[t]==i[time[item]]+x[t]+y[t]-demand[t]

prob.writeLP("single_product_lot.lp")
prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total Cost of Production = ", value(prob.objective))