import numpy as np
from itertools import count
from pyomo.environ import *


# =========================== Parameters ======================================
np.random.seed(1)
TOL = 1e-6
W_roll = 100 # roll width
I = list(range(5)) # item set
w = np.random.randint(1, 50, len(I)).tolist() # width of each item
d = np.random.randint(1, 50, len(I)).tolist() # demand of each item
patterns = np.diag([W_roll // w[i] for i in I]).tolist() # initial patterns
K = list(range(20)) # the known upper bound on the number of rolls needed (index k)

# ========================= Weak Problem ====================================
modelw = ConcreteModel('weak')
modelw.smallrolls = Set(initialize=I)
modelw.rolls = Set(initialize=K)

modelw.x = Var(modelw.smallrolls, modelw.rolls, domain=NonNegativeIntegers)
modelw.y = Var(modelw.rolls, domain=Boolean)

@modelw.Constraint(modelw.smallrolls)
def req(modelw, i):
    return sum([modelw.x[i, k] for k in modelw.rolls]) == d[i]

@modelw.Constraint(modelw.rolls)
def width(modelw, k):
    return sum([modelw.x[i, k] * w[i] for i in modelw.smallrolls]) <= W_roll * modelw.y[k]

@modelw.Objective(sense=minimize)
def cost(modelw):
    return sum([1 * modelw.y[k] for k in modelw.rolls])

resultsw = SolverFactory('gurobi').solve(modelw)

print(resultsw)

for i in modelw.smallrolls:
    print(f"{i}, {sum(modelw.x[i, k].value for k in modelw.rolls)}")

# ========================= Master Problem ====================================
def generate_master_problem(type):
    model = ConcreteModel('master')
    model.patterns = Set(initialize=range(len(patterns)))
    model.smallrolls = Set(initialize=I)
    if type == 'float':
        model.x = Var(model.patterns, domain=NonNegativeReals)
    else:
        model.x = Var(model.patterns, domain=NonNegativeIntegers)

    @model.Constraint(model.smallrolls)
    def req(model, i):
        return sum([patterns[p][i] * model.x[p] for p in model.patterns]) == d[i]

    @model.Objective(sense=minimize)
    def cost(model):
        return sum([1 * model.x[p] for p in model.patterns])

    model.dual = Suffix(direction=Suffix.IMPORT)
    return model

model = generate_master_problem('float')

# ======================= Subproblem and Iteration ============================
for iter_count in count():
    results = SolverFactory('gurobi').solve(model)

    print(results)

    for p in model.patterns:
        if model.x[p].value > 0:
            print(f"{model.x[p]}, {model.x[p].value}")

    price = [model.dual[model.req[i]] for i in I]
    print(f'Price = {price}')

    sp = ConcreteModel('subproblem') # Subproblem
    sp.smallrolls = Set(initialize=I)
    sp.use = Var(sp.smallrolls, domain=NonNegativeIntegers)
    @sp.Constraint()
    def width(sp):
        return sum([sp.use[i] * w[i] for i in sp.smallrolls]) <= W_roll

    @sp.Objective(sense=maximize)
    def dual(sp):
        return sum([price[i] * sp.use[i] for i in sp.smallrolls])

    resultssp = SolverFactory('gurobi').solve(sp)
    print(resultssp)

    for i in sp.smallrolls:
        if sp.use[i].value > 0:
            print(f"{sp.use[i]}, {sp.use[i].value}")

    min_rc = 1 - value(sp.dual)
    if min_rc < -TOL:
        patterns.append([int(sp.use[i].value) for i in I])
        print(f'min reduced cost = {min_rc:.4f};'
                    f' new pattern: {patterns[-1]}')
        model = generate_master_problem('float')
    else:
        break

# ====================== Relaxed Model Result =================================
model = generate_master_problem('float')
results = SolverFactory('gurobi').solve(model, tee=True)
print(results)

for p in model.patterns:
    if model.x[p].value > 0:
        print(f"{model.x[p]}, {model.x[p].value}")

# ====================== Integer Model Result =================================
model = generate_master_problem('integer')
results = SolverFactory('gurobi').solve(model, tee=True)
print(results)

for i in model.smallrolls:
    print(f"{i}, {sum(patterns[p][i] * model.x[p].value for p in model.patterns)}")
