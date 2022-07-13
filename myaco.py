# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:44:11 2020

@author: Wariat
"""

import time
import math
import random
'''
x=punkty
alpha
beta
it=liczba iteracji
ants=liczba mrówek
q=zostawiane feromony przez mrówki
rho=współczynnik zanikania feromonu
q1=początkowa wartosć feromonu
'''

class myaco(object):
    def __init__(self,x,alpha=1.0,beta=3.0,it=100,ants=10,q=1.0,rho=0.8,q1=0.1):
        self.world=world(x,q1,rho,alpha,beta,q)
        self.colony=colony(ants)
        self.it=it
        self.best=math.inf
        self.best_way=[]
    def solver(self):
        for i in range(self.it):
            self.colony.solve(self.world)
            if self.colony.best<self.best:
                self.best=self.colony.best
                self.best_way=self.colony.best_way.copy()
            self.world.decay()
        self.print()
    def print(self):
        print("dystans:" + str(self.best))
        #print("trasa:" + str(self.best_way))
class colony(object):
    def __init__(self,ants):
        self.ants=[]
        for i in range(ants):
            self.ants.append(ant())
    def solve(self,world):
        l=[]
        for i in self.ants:
            l.append(i.solve(world))
        self.best=min(l)
        ind=l.index(self.best)
        self.best_way=self.ants[ind].way
class ant(object):
    def __init__(self):
        pass
    def solve(self,world):
        self.way=[]
        p=[]
        for i in world.edges:
            p.append(i.w)
        x=random.choices(world.edges,weights=p)[0]
        d=x.dyst
        self.way.append(x.x)
        x.update()
        for i in range(world.l-2):
            pr=[]
            for j in x.n:
                if j.y in self.way:
                    pr.append(0)
                else:
                    pr.append(j.w)
            x=random.choices(x.n,weights=pr)[0]
            self.way.append(x.x)
            d=d+x.dyst
            x.update()
        for j in x.n:
            if j.y==self.way[0]:
                x=j
                break;
        self.way.append(x.x)
        d=d+x.dyst
        x.update()
        return d
class world(object):
    def __init__(self,x,q1,rho,alpha,beta,q):
        self.edges=[]
        self.l=len(x)
        for i in range(len(x)):
            for j in range(len(x)):
                if i!=j:
                    self.edges.append(edge(x[i],x[j],q1,rho,alpha,beta,q))
        for i in self.edges:
            for j in self.edges:
                if i!=j:
                    if i.y==j.x:
                        i.n.append(j)
        self.el=len(self.edges)
    def decay(self):
        for i in self.edges:
            i.decay()
class edge(object):
    def __init__(self,i,j,q1,rho,alpha,beta,q):
        self.x=i
        self.y=j
        self.n=[]
        self.pheromone=q1
        self.rho=rho
        self.q=q
        self.dyst=eu(self.x,self.y)
        self.alpha=alpha
        self.beta=beta
        self.w=math.pow(self.pheromone,self.alpha)*math.pow(1/self.dyst,self.beta)
    def decay(self):
        self.pheromone=self.pheromone*(1.0-self.rho)
        self.w=math.pow(self.pheromone,self.alpha)*math.pow(1/self.dyst,self.beta)
    def update(self):
        self.pheromone=self.pheromone+self.q
def eu(x,y):
    return math.sqrt((y[0]-x[0])*(y[0]-x[0])+(y[1]-x[1])*(y[1]-x[1]))

    
    
    
    