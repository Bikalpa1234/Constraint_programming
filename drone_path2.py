# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 20:11:57 2020

@author: Aman
"""

from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        l=[self.Value(u) for u in self.__variables]
        print(l)

    def solution_count(self):
        return self.__solution_count

def count_paths(start, end):
    
    #Stores no. of possible paths
    count=0
    av_path=[[1,4],
             [0,5,2],
             [1,6,3],
             [2,7],
             [0,5,8],
             [1,4,6,9],
             [2,5,7,10],
             [3,6,11],
             [4,9,12],
             [5,8,10,13],
             [6,9,11,14],
             [7,10,15],
             [8,13,16],
             [9,12,14,17],
             [10,13,15,18],
             [11,14,19],
             [12,17],
             [13,16,18],
             [14,17,19],
             [15,18]]
    
    for n in range(2,5):
        model=cp_model.CpModel()

        path=[model.NewIntVar(0, 19, 'path%i' %j) for j in range(n+1)]
        for i in range(1,n+1):
            for j in range(20):
                b=model.NewBoolVar('')
                model.Add(path[i-1]==j).OnlyEnforceIf(b)
                model.Add(path[i-1]!=j).OnlyEnforceIf(b.Not())
                model.AddLinearExpressionInDomain(path[i], 
                        cp_model.Domain.FromValues(av_path[j])).OnlyEnforceIf(b)
                
        model.AddAllowedAssignments([path[0], path[-1]], [(start, end)])
        for x in path[1:-1]:
            model.AddForbiddenAssignments([x], [(8,),(10,),(13,)])
            
        sol_printer=VarArraySolutionPrinter(path)
        solver=cp_model.CpSolver()

        status=solver.SearchForAllSolutions(model, sol_printer)
        count+=sol_printer.solution_count()

    return count

loc=[8,10,13]
cur_pos=0

for i in range(3):
    no_of_count=[]
    for j in loc:
        no_of_count.append(count_paths(cur_pos, j))
    cur_pos=loc[no_of_count.index(min(no_of_count))]
    loc.remove(cur_pos)
    print(cur_pos)

        
        