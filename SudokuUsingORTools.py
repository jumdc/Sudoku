# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:10:13 2020

@author: julie
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import *

from ortools.sat.python import cp_model


def createGrille(niveau):
    #Creates the model
    model= cp_model.CpModel()
    numVals=9
    nbrCases=0;
    if niveau=="très difficile":
        nbrCases=17
    if niveau=="difficile":
        nbrCases=26
    if niveau=="moyen":
        nbrCases=33
    if niveau=="facile":
        nbrCases=40
    if niveau=="débutant":
        nbrCases=50
    G= [[0] * 9 for i in range(9)]
    A= [[0] * 9 for i in range(9)]
    compteur=0
    #on cherche aléatoirement la position des n chiffres que l'on souhaite placés
    #leur position est modélisé par un 1
    while compteur<nbrCases :
        ligne=randint(0,8)
        colonne=randint(0,8)
        if G[ligne][colonne]==0:
            G[ligne][colonne]=1
            compteur+=1
    cellSize=3
    cell=range(cellSize)
    for ligne in range(9):
        for colonne in range(9):
            A[ligne][colonne]=model.NewIntVar(0,numVals,'A[%i][%a]' %(ligne,colonne))
               
    #contraintes
    #les éléments mis sur une ligne de peuvent pas être identiques 
    for ligne in range(9):
        diff=[]
        for colonne in range(9):
            if G[ligne][colonne]==1:
                diff.append(A[ligne][colonne])
            else:
                model.Add(A[ligne][colonne]==0) #on ne veut pas appliquer les contraintes aux 0 qui représentent des cases vides
        model.AddAllDifferent(diff)
    #aucune même valeur sur une colonne
    for colonne in range(9):
        diff=[]
        for ligne in range(9):
            if G[ligne][colonne]==1:
                diff.append(A[ligne][colonne])
        model.AddAllDifferent(diff)
       
    #aucune même valeur dans les sous-carrées de 3*3
    for i in cell:
        for j in cell:
            oneCell=[]
            for di in cell:
                for dj in cell:
                    if G[i*cellSize+di][j*cellSize+dj]==1:
                        oneCell.append(A[i*cellSize+di][j*cellSize+dj])
            model.AddAllDifferent(oneCell)   
    
    #solveur
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE:
        R=[]
        for ligne in range(9):
            R.append([solver.Value(A[ligne][j]) for j in range(9)])
            print([solver.Value(A[ligne][j]) for j in range(9)])
    return R
        
def Sudoku(grille):
    #Creates the model
    model= cp_model.CpModel()
    #Create the Variables
    numVals= 9
    A= [[0] * 9 for i in range(9)]
    ##remplir en prenant en compte les cases déjà remplies dans la grille sinon tourne en boucle 
    cellSize=3
    cell=range(cellSize)
    for ligne in range(9):
        for colonne in range(9):
            A[ligne][colonne]=model.NewIntVar(1,numVals,'A[%i][%a]' %(ligne,colonne))
            if grille[ligne][colonne]!=0:
                model.Add( A[ligne][colonne]==grille[ligne][colonne])

    #create the constraints
    #aucune même valeur une ligne
    for ligne in range(9): #on le fait pour chaque ligne
        for i in range(9):
            j=i+1
            while(j<9):
                model.Add(A[ligne][i]!=A[ligne][j])
                j=j+1
        

    #aucune même valeur sur une colonne
    for colonne in range(9):
        for i in range(9):
            j=i+1
            while(j<9):
                model.Add(A[i][colonne]!=A[j][colonne])
                j+=1
                
    #aucune même valeur dans les sous-carrées de 3*3
    for i in cell:
        for j in cell:
            oneCell=[A[i*cellSize+di][j*cellSize+dj]
            for di in cell
            for dj in cell
            ]
        model.AddAllDifferent(oneCell)
            
    #solveur
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(status)
    if status == cp_model.FEASIBLE:
        for ligne in range(9):
            print([solver.Value(A[ligne][j]) for j in range(9)])
    
    
niveau="facile"
R=createGrille(niveau)
Sudoku(R)