# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

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
    items : list[int] = field(default_factory=list)
    bound : float = 0

    def __init__(self, level, profit, weight, items):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.items = items
        
            
def get_bound(node, n, price, weight, capacity, p_per_weight):
    if node.weight >= capacity:
        return 0
    else:
        result = node.profit
        j = node.level + 1
        totweight = node.weight
        while j <= n-1 and totweight + weight[j] <= capacity:
            totweight += weight[j]
            result += price[j]
            j += 1
        k = j
        if k <= n-1:
            result = result + (capacity - totweight) * p_per_weight[k]
        return result


def branch_and_bound(n, price, weight, capacity, p_per_weight):
    nodes_generated = 0
    pq = Priority_Queue()

    v = Node(-1, 0, 0, []) # v initialized to be the root with level = 0, profit = $0, weight = 0
    nodes_generated+=1
    maxprofit = 0 # maxprofit initialized to $0
    v.bound = get_bound(v, n, price, weight, capacity, p_per_weight)
    #print("v.bound = ", v.bound)

    pq.insert(v)

    while pq.length != 0:
        
        v = pq.remove() #remove node with best bound

        if v.bound > maxprofit: #check if node is still promising
            #set u to the child that includes the next item
            u = Node(level = v.level + 1,
                     profit = v.profit + price[v.level + 1],
                     weight = v.weight + weight[v.level + 1],
                     items = []
                    )
            nodes_generated+=1
            #create u's list from v's list and add the new item
            u.items = v.items.copy() + [u.level]
            if u.weight <= capacity and u.profit > maxprofit: 
                #update maxprofit
                maxprofit = u.profit
                bestitems = u.items
            u.bound = get_bound(u, n, price, weight, capacity, p_per_weight)
            print(f'u0 : {u}')       

            if u.bound > maxprofit:
                pq.insert(u)

            #set u to the child that does not include the next item
            u2 = Node(u.level, v.profit, v.weight, v.items.copy())
            nodes_generated+=1
            u2.bound = get_bound(u2, n, price, weight, capacity, p_per_weight)
            print(f'u2 : {u2}')

            if u2.bound > maxprofit:
                pq.insert(u2)

    print("\nEND maxprofit = ", maxprofit, "nodes generated = ", nodes_generated)
    print("bestitems = ", bestitems)
    return bestitems

if __name__ == "__main__":
    pass
