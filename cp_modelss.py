# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 19:58:57 2020

@author: Aman
"""

import numpy as np
from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.all_sol=[]

    def on_solution_callback(self):
        self.__solution_count += 1
        l=[self.Value(u) for u in self.__variables]
        self.all_sol.append(l)

    def solution_count(self):
        return self.__solution_count

def one(n=10):
    """
    0<x<4 
    0<y<=10 
    x->int y->int
    x+y>=5
    """
    
    model=cp_model.CpModel()
    #declaring variable
    x=model.NewIntVar(1, 3, 'x')
    y=model.NewIntVar(1,n,'y')
    #constraint
    model.Add(x+y>=5)
    
    #solution printer
    sol_printer=VarArraySolutionPrinter([x,y])
    #solver
    solver=cp_model.CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    return sol_printer.all_sol

def two():
    """
     two
    +two
    ----
    four
    """
    model=cp_model.CpModel()
    #declaring vars
    t=model.NewIntVar(1,9, 't')
    w=model.NewIntVar(0,9,'w')
    o=model.NewIntVar(0,9, 'o')
    f=model.NewIntVar(1,9, 'f')
    u=model.NewIntVar(0,9, 'u')
    r=model.NewIntVar(0,9, 'r')
    var=[t, w, o, f, u, r]
    #constraint
    model.AddAllDifferent(var)
    #constraint2
    model.Add(2*(100*t + 10*w + o) == 1000*f+ 100*o +10*u +r)
    sol_printer=VarArraySolutionPrinter(var)
    solver=cp_model.CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    return sol_printer.all_sol

def three():
    """
    10a+4.5b+c+2.5d<=300
    2a+1.4b+.6c+.9d<=200
    8a+6.8b+4c+3d<=300
    Max. F=20a+16b+9c+7d
    """
    model=cp_model.CpModel()
    #variable
    a=model.NewIntVar(0, 30, 'a')
    b=model.NewIntVar(0, 30, 'b')
    c=model.NewIntVar(0, 100, 'c')
    d=model.NewIntVar(0, 100, 'd')
    var=[a,b,c,d]
    #constraint
    model.Add(a*100 +b*45 +c*10 +d *25 <=3000)
    model.Add(a*20+b*14+c*6+d*9<=2000)
    model.Add(a*80+b*68+c*40+d*30<=3000)
    model.Maximize(a*20 + b*16 + c* 9 +d*7)
    solver=cp_model.CpSolver()
    # sol_printer=VarArraySolutionPrinter(var)
    # status=solver.SearchForAllSolutions(model, sol_printer)
    # return sol_printer.all_sol
    status=solver.Solve(model)
    if status==cp_model.OPTIMAL:
        print('obj value = {}'.format(solver.ObjectiveValue()))
        print("""
              a={}
              b={}
              c={}
              d={}
              """.format(solver.Value(a),
              solver.Value(b), 
              solver.Value(c), 
              solver.Value(d), 
              ))
    
def four(total=60):
    """
    Gives all possible combination of [1,2,5,10,20] which 
    adds up to 'total'.
    Returning change/cash problem.

    Parameters
    ----------
    total : TYPE, optional
        DESCRIPTION. The default is 60.

    Returns
    -------
    None.
    """
    model=cp_model.CpModel()
    #variable
    a=model.NewIntVar(0, total, 'a')
    b=model.NewIntVar(0, total//2, 'b')
    c=model.NewIntVar(0, total//5, 'c')
    d=model.NewIntVar(0, total//10, 'd')
    e=model.NewIntVar(0, total//20, 'e')

    var=[a,b,c,d,e]
    #constraint
    model.Add(a + 2*b + 5*c +10*d +20*e ==total)
    for v in var:
        model.AddModuloEquality(0, v, 2)

    sol_printer=VarArraySolutionPrinter(var)
    solver=cp_model.CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    return sol_printer.all_sol

def mix():
    """
    Qn1          [[90,100,100,90,100],
                 [40,100,100,60,75],
                 [6.5,98.1,100,40,55],
                 [3,20.7,93.2,20,35],
                 [1.2,12.2,58.7,12,22],
                 [.5,3.3,27.4,5,10]]
    
    Qn2
    """
    qn=np.array( [[90,100,100,90,100],
                 [40,100,100,60,75],
                 [6.5,98.1,100,40,55],
                 [3,20.7,93.2,20,35],
                 [1.2,12.2,58.7,12,22],
                 [.5,3.3,27.4,5,10]])
    qn=(qn*10).astype(np.int64)
    model=cp_model.CpModel()
    unit=100
    #variable
    a=model.NewIntVar(0, unit, 'a')
    b=model.NewIntVar(0, unit, 'b')
    c=model.NewIntVar(0, unit, 'c')
    var=[a,b,c]
    #constraint1
    model.Add(a+b+c==unit)
    #constraint 2
    for n in qn:
        lb=int(n[3]*unit)
        ub=int(n[4]*unit) #Domain must take int args. not np.int32 or np.int64
        model.AddLinearConstraint(n[0]*a+n[1]*b+n[2]*c,lb,ub)
    sol_printer=VarArraySolutionPrinter(var)
    solver=cp_model.CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    return sol_printer.all_sol


one(5)