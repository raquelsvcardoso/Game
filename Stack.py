# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 14:12:49 2019

@author: Raquel Cardoso PG38698
"""

class Stack:
    
    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)
        
    def is_empty(self):
        return self.items == []
    
    def push(self, item): #insere um novo elemento no inicio da stack
        self.items.append(item)

    def top(self): #retorna o elemento que está no inicio da stack
        if len(self.items) > 0:
            return self.items[-1]

    def pop(self): #remove o elemento que está no inicio da stack
        return self.items.pop()
    
    def size(self): #retorna o tamanho da stack
        return len(self.items)

