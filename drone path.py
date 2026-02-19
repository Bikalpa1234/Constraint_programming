# -*- coding: utf-8 -*-
"""
Created on Wed May 20 19:48:10 2020

@author: Aman
"""

from ortools.sat.python.cp_model import*

class VarArraySolutionPrinter(CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        l=[self.Value(u) for u in self.__variables]
        print(l)

    def solution_count(self):
        return self.__solution_count



def one():
    model=CpModel()
    x=model.NewIntVar(1, 3, 'x')
    y=model.NewIntVar(0,9, 'y')
    model.Add(x + y>=5)
    sol_printer=VarArraySolutionPrinter([x, y])
    solver=CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    print(sol_printer.solution_count())
    
def two():
    model=CpModel()
    t=model.NewIntVar(1,9, 't')
    w=model.NewIntVar(0,9,'w')
    o=model.NewIntVar(0,9, 'o')
    f=model.NewIntVar(1,9, 'f')
    u=model.NewIntVar(0,9, 'u')
    r=model.NewIntVar(0,9, 'r')
    var=[t, w, o, f, u, r]
    model.AddAllDifferent(var)
    model.Add(2*(100*t + 10*w + o) == 1000*f +100*o +10*u +r)
    sol_printer=VarArraySolutionPrinter(var)
    solver=CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    print(sol_printer.solution_count())

def three(total=60):
    """
    Gives all possible combination of [1,3,5,10,20] which 
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
    model=CpModel()
    a=model.NewIntVar(0, total, 'a')
    b=model.NewIntVar(0, total//3, 'b')
    c=model.NewIntVar(0, total//5, 'c')
    d=model.NewIntVar(0, total//10, 'd')
    e=model.NewIntVar(0, total//20, 'e')
    var=[a,b,c,d,e]
    model.Add(a + 3*b + 5*c +10*d +20*e ==total)
    sol_printer=VarArraySolutionPrinter(var)
    solver=CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    print(sol_printer.solution_count())

def four():
    model=CpModel()
    a=model.NewIntVar(0, 37, 'a')
    b=model.NewIntVar(0, 44, 'b')
    c=model.NewIntVar(0, 75, 'c')
    d=model.NewIntVar(0, 100, 'd')
    var=[a,b,c,d]
    model.Add(a*100 +b*45 +c*10 +d *25 <=3000)
    model.Add(a*20+b*14+c*6+d*9<=2000)
    model.Add(a*80+b*68+c*40+d*30<=3000)
    model.Maximize(a*20 + b*16 + c* 9 +d*7)
    solver=CpSolver()
    status=solver.Solve(model)
    if status==OPTIMAL:
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
    
def five():
    x=6
    y=9
    model=CpModel()
    a=model.NewIntVarFromDomain(Domain.FromValues([1,2]),'a')
    b=model.NewIntVar(4,4,'b')
    c=model.NewIntVar(5,7,'c')
    d=model.NewIntVar(8,9,'d')
    var=[a,b,c,d]
    bol=model.NewBoolVar('')
    model.Add(a==1).OnlyEnforceIf(bol)
    model.Add(a==2).OnlyEnforceIf(bol.Not())
    model.AddLinearExpressionInDomain(var[3], Domain.FromValues([8])).OnlyEnforceIf(bol)
    model.AddLinearConstraint(c,x,y).OnlyEnforceIf(bol.Not())
    sol_printer=VarArraySolutionPrinter([a,b,c,d,bol])
    solver=CpSolver()
    status=solver.SearchForAllSolutions(model, sol_printer)
    print(sol_printer.solution_count())

def six():
    model=CpModel()
    av_path=[[10],
             [2,3],
             [1,4],
             [1,4,5],
             [2,3,6],
             [3,6,7],
             [4,5,8],
             [5,8],
             [6,7,9],
             [8,11],
             [0,11],
             [9,10]]
    path=[model.NewIntVar(0,11,'drone%i' %i) for i in range(8)]
    
    for i in range(1,8):
        for j in range(12):
            b=model.NewBoolVar('')
            model.Add(path[i-1]==j).OnlyEnforceIf(b)
            model.Add(path[i-1]!=j).OnlyEnforceIf(b.Not())
            model.AddLinearExpressionInDomain(path[i], 
                    Domain.FromValues(av_path[j])).OnlyEnforceIf(b)
            
    model.AddAllowedAssignments([path[0], path[-1]], [(10, 4)])

    sol_printer=VarArraySolutionPrinter(path)
    solver=CpSolver()

    status=solver.SearchForAllSolutions(model, sol_printer)
    print(sol_printer.solution_count())

    
        
    

