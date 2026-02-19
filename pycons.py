# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 13:04:35 2020



import numpy as np
from itertools import product
import constraint

def one(n=10):
    """
    0<x<4 
    0<y<=10 
    x->int y->int
    x+y>=5
    """
    pro=constraint.Problem()
    #declaring variable and its domain
    pro.addVariable('x', [3,5,9])
    pro.addVariable('y', range(1,n+1))

    #constraint
    pro.addConstraint(lambda x,y: x+y>=5,['x','y'])
    #con2
    pro.addConstraint(lambda y: y%2==0,'y')
    sol = pro.getSolutions()
    return sol

def two():
    """
     two
    +two
    ----
    four
    """
    pro=constraint.Problem()
    #variable
    var1=['t','f']
    var2=['w','o','u','r']
    pro.addVariables(var1, range(1,10))
    pro.addVariables(var2, range(0,10))
    #constraint1
    pro.addConstraint(constraint.AllDifferentConstraint())
    #constraint2
    def add(t,w,o,f,u,r):
        return 2*(t*100+w*10+o)==f*1000+o*100+u*10+r
    pro.addConstraint(add,['t','w','o','f','u','r'])
    sol=pro.getSolutions()
    return sol

def three():
    """
    10a+4.5b+c+2.5d<=300
    2a+1.4b+.6c+.9d<=200
    8a+6.8b+4c+3d<=300
    Max. F=20a+16b+9c+7d
    """
    pro=constraint.Problem()
    #variable
    var=['a','b','c','d']
    pro.addVariables(var, range(0,100))
    #constraint
    pro.addConstraint(lambda a,b,c,d: a*10 +b*4.5 +c*1 +d *2.5 <=300,var)
    pro.addConstraint(lambda a,b,c,d: a*2+b*1.4+c*0.6+d*0.9<=200,var)
    pro.addConstraint(lambda a,b,c,d: a*8+b*6.8+c*4+d*3<=300,var)
    sol=pro.getSolutions()
    obj_F=np.array([x['a']*20+x['b']*16+x['c']*9+x['d']*7 for x in sol])   
    return np.max(obj_F), sol[np.argmax(obj_F)]
    #return sol

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
    pro=constraint.Problem()
    #var
    var={'a':1,'b':2,'c':5,'d':10,'e':20}
    for x,y in var.items():
        pro.addVariable(x, range(0,total//y+1))
    #constraint
    pro.addConstraint(lambda a,b,c,d,e: a+2*b+5*c+10*d+20*e==total, var)
    sol=pro.getSolutions()
    return sol

def calcdoku():
    """
    https://brilliant.org/daily-problems/calcdoku-13/
    """
    pro=constraint.Problem()
    #var
    var=np.array([['a%i%i' %(i,j) for j in range(5)]for i in range(5)])
    for i in range(5):
        pro.addVariables(var[i].tolist(), range(1,6))
        pro.addConstraint(constraint.AllDifferentConstraint(), 
                          var[i].tolist())
      
    for i in range(5):
        pro.addConstraint(constraint.AllDifferentConstraint(), 
                          var[:,i].tolist())
        
    pro.addConstraint(lambda x,y: abs(x-y)==2, var[0,0:2].tolist())
    
    pro.addConstraint(lambda a,b,c,d: a*b*c*d==32, ['a02','a03',
                                                          'a13', 'a14'])
    
    pro.addConstraint(constraint.ExactSumConstraint(10), 
                      var[1:2,:3].flatten().tolist())
    
    pro.addConstraint(constraint.ExactSumConstraint(17),
                      np.append(var[2], 'a33').tolist())
    
    pro.addConstraint(lambda a,b,c: a*b*c==80, ['a30','a40','a41'])
    
    pro.addConstraint(constraint.ExactSumConstraint(6), ['a34','a43','a44']) 
    
    pro.addConstraint(lambda a,b: a/b==5 or a/b==0.2, var[3:,2].tolist())

    sol=pro.getSolutions()
    return sol

