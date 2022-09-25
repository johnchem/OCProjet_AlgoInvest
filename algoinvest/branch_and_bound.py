
# -*- coding: utf-8 -*-
"""
Author: Nathan Rice
0-1 Knapsack Problem using best first branch and bound method 
Returns maxprofit with list storing the index position of the items in the best solution.
The profit is maximized while staying under the weight limit.
This program uses a priority queue to store the nodes ordered by best bound,
the node with the highest bound value is returned when removing from the priority queue.
The best first approach arrives at an optimal solition faster than breadth first search.
"""
#examples
# W = 13
# i  pi  wi pi/wi
# 1 $20  2   10
# 2 $30  5   6
# 3 $35  7   5
# 4 $12  3   4
# 5 $3   1   3
#problem definition
# n = 5 #items given
# W = 13 # capacity of knapsack
# p = [0, 20, 30, 35, 12, 3] # profit of each item (starts with item 0 = $0)
# w = [0, 2, 5, 7, 3, 1] # weight of each item
# p_per_weight = [0, 10, 6, 5, 4, 3] #price per weight

#example 6.1
# items are ordered by price per weight
# n = 4
# W = 16
# p = [40, 30, 50, 10]
# w = [2, 5, 10, 5]
# p_per_weight = [20, 6, 5, 2]
from dataclasses import dataclass

class Priority_Queue:
    def __init__(self):
        self.pqueue = []
        self._length = 0

    @property
    def length(self):
        return len(self.pqueue)
    
    @length.setter
    def length(self, value):
        self._length = value

    def insert(self, node):
        i = 0
        while i < len(self.pqueue):
            if self.pqueue[i].bound > node.bound:
                break
            i+=1
        self.pqueue.insert(i,node)
        
    def insert_bis(self,node):
        self.pqueue.append(node)
        self.pqueue.sort(lambda x: x.bound, reverse = True)

    def print_pqueue(self):
        for i in list(range(len(self.pqueue))):
            print ("pqueue",i, "=", self.pqueue[i].bound)
                    
    def remove(self):
        try:
            result = self.pqueue.pop()
        except: 
            print("Priority queue is empty, cannot pop from empty list.")
        else:
            return result

@dataclass       
class Node:
    level : int
    profit : float
    weight : float
    items : list() = []
    bound : float = 0

    def __init__(self, level, profit, weight):
        self.level = level
        self.profit = profit
        self.weight = weight
        
            
def get_bound(node, n, price, weight, capacity, p_per_weight):
    if node.weight >= capacity:
        return 0
    else:
        result = node.profit
        j = node.level + 1
        totweight = node.weight
        while j <= n-1 and totweight + weight[j] <= capacity:
            totweight = totweight + weight[j]
            result = result + price[j]
            j+=1
        k = j
        if k<=n-1:
            result = result + (capacity - totweight) * p_per_weight[k]
        return result

def branch_and_bound(n, price, weight, capacity, p_per_weight):
    nodes_generated = 0
    pq = Priority_Queue()

    v = Node(-1, 0, 0) # v initialized to be the root with level = 0, profit = $0, weight = 0
    nodes_generated+=1
    maxprofit = 0 # maxprofit initialized to $0
    v.bound = get_bound(v, n, price, weight, capacity, p_per_weight)
    #print("v.bound = ", v.bound)

    pq.insert(v)

    while pq.length != 0:
        
        v = pq.remove() #remove node with best bound
    #    print("\nNode removed from pq.")
    #    print("Priority Queue: ") 
    #    pq.print_pqueue()
        
    #    print("\nmaxprofit = ", maxprofit)
    #    print("Parent Node: ")
    #    print("v.level = ", v.level, "v.profit = ", v.profit, "v.weight = ", v.weight, "v.bound = ", v.bound, "v.items = ", v.items)

        if v.bound > maxprofit: #check if node is still promising
            #set u to the child that includes the next item
            u = Node(level = v.level + 1,
                     profit = v.profit + price[u.level],
                     weight = v.weight + weight[u.level]
                    )
            nodes_generated+=1
            
            #create u's list from v's list and add the new item
            u.items = v.items.copy() + list(u.level)
    #        print("child that includes the next item: ")
    #        print("Child 1:")
    #        print("u.level = ", u.level, "u.profit = ", u.profit, "u.weight = ", u.weight)
    #        print("u.items = ", u.items)
            if u.weight <= capacity and u.profit > maxprofit: 
                #update maxprofit
                maxprofit = u.profit
    #            print("\nmaxprofit updated = ", maxprofit)
                bestitems = u.items
    #            print("bestitems = ", bestitems)
            u.bound = get_bound(u, n, price, weight, capacity, p_per_weight)
    #        print("u.bound = ", u.bound)
            if u.bound > maxprofit:
                pq.insert(u)
    #            print("Node u1 inserted into pq.")
    #            print("Priority Queue : ") 
    #            pq.print_pqueue()
            #set u to the child that does not include the next item
            u2 = Node(u.level, v.profit, v.weight)
            nodes_generated+=1
            u2.bound = get_bound(u2, n, price, weight, capacity, p_per_weight)
            u2.items = v.items.copy()
    #        print("child that doesn't include the next item: ")
    #        print("Child 2:")
    #        print("u2.level = ", u2.level, "u2.profit = ", u2.profit, "u2.weight = ", u2.weight, "u2.bound = ", u2.bound)
    #        print("u2.items = ", u2.items)
            if u2.bound > maxprofit:
                pq.insert(u2)
    #            print("Node u2 inserted into pq.")
    #            print("Priority Queue : ") 
    #            pq.print_pqueue()
    print("\nEND maxprofit = ", maxprofit, "nodes generated = ", nodes_generated)
    print("bestitems = ", bestitems)
    return bestitems

if __name__ == "__main__":
    pass
