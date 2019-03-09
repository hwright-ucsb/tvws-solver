from gurobipy import *
import random
from array import *

matrix = [[0]*3 for i in range(3)]

for i in range(3):
    for j in range(3):
        matrix[i][j] = [random.uniform(33.15564023, 33.21248565),random.uniform(-116.7374455, -116.6731731)]

# Problem Data
# Population in each region
pop = [523, 690, 420, 1010, 1200, 850, 400, 1008, 950]
# Regions covered by each tower
sites = [[0,1,5], [0,7,8], [2,3,4,6], [2,5,6],
         [0,2,6,7,8], [3,4,8]]
# Cost to build tower (in millions of dollars)
cost = [4.2, 6.1, 5.2, 5.5, 4.8, 9.2]
# Allocated budget (in millions of dollars)
budget = 20

numR = len(pop) # Number of regions
numT = len(sites) # Number of sites for towers

m = Model()

t = {} # Binary variables for each tower
r = {} # Binary variable for each region

for i in range(numT):
  t[i] = m.addVar(vtype=GRB.BINARY, name="t%d" % i)

for j in range(numR):
  r[j] = m.addVar(vtype=GRB.BINARY, name="r%d" % j)

m.update()

for j in range(numR):
  m.addConstr(quicksum(t[i] for i in range(numT) if j in sites[i]) >= r[j])

m.addConstr(quicksum( cost[i]*t[i] for i in range(numT) ) <= budget)

m.setObjective(quicksum( pop[j]*r[j] for j in range(numR) ), GRB.MAXIMIZE)

m.optimize()