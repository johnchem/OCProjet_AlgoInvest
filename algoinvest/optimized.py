# -*- coding: utf-8 -*-

from collections import namedtuple
from dataclasses import dataclass, field
from turtle import pos

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
        
    def __repr__(self):
        return "pqueue \n" + "\n".join([str(round(x.bound,2)) for x in self.pqueue])
        
                    
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

    def __repr__(self):
        return (f'branche : {" ".join([str(x) for x in self.items])}\n' +
                f'level : {self.level} profit : {round(self.profit,2)} cout : {self.weight}')
        
            
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


def branch_and_bound(dataset, capacity, sort_fct):
    '''
    
    '''
    dataset.sort(key=sort_fct, reverse=True)
    
    n = len(dataset)
    weight = [x.value for x in dataset]
    price = [x.roi*x.value for x in dataset]
    p_per_weight = [x.roi for x in dataset]
    
    nodes_generated = 0
    pq = Priority_Queue()

    current_node = Node(-1, 0, 0, []) # v initialized to be the root with level = 0, profit = $0, weight = 0
    nodes_generated+=1
    roi_max = 0 # maxprofit initialized to $0
    current_node.bound = get_bound(current_node, n, price, weight, capacity, p_per_weight)
    #print("v.bound = ", v.bound)

    pq.insert(current_node)

    while pq.length != 0:
        # print(pq)
        current_node = pq.remove() #remove node with best bound
        print(f'\ncurrent_node : \n{current_node}')

        if current_node.bound > roi_max: #check if node is still promising
            #set u to the child that includes the next item
            pos_node = Node(level = current_node.level + 1,
                            profit = current_node.profit + price[current_node.level + 1],
                            weight = current_node.weight + weight[current_node.level + 1],
                            items = []
                            )
            nodes_generated+=1
            print(f'\npos_node : \n{pos_node}')
            #create u's list from v's list and add the new item
            pos_node.items = current_node.items.copy() + [pos_node.level]
            if pos_node.weight <= capacity and pos_node.profit > roi_max: 
                #update maxprofit
                total_cost = pos_node.weight
                roi_max = pos_node.profit
                best_investment = pos_node.items
            pos_node.bound = get_bound(pos_node, n, price, weight, capacity, p_per_weight)
            # print(f'pos_node : {pos_node}')       

            if pos_node.bound > roi_max:
                print('pos_node dans la file')
                pq.insert(pos_node)

            #set u to the child that does not include the next item
            neg_node = Node(pos_node.level, current_node.profit, current_node.weight, current_node.items.copy())
            nodes_generated+=1
            neg_node.bound = get_bound(neg_node, n, price, weight, capacity, p_per_weight)
            print(f'\nneg_node : \n{neg_node}')
            # print(f'neg_node : {neg_node}')

            if neg_node.bound > roi_max:
                print('neg_node dans la file')
                pq.insert(neg_node)

    best_investment = [dataset[x] for x in best_investment]
    # print("\nEND maxprofit = ", roi_max, "nodes generated = ", nodes_generated)
    # print("bestitems = ", best_investment)
    return best_investment, round(total_cost, 2), round(roi_max, 2)

if __name__ == "__main__":
    share = namedtuple('share',('name', 'value', 'roi'))
    raw_set = [['Share-DUPH',"10.01","12.25"],
               ['Share-GTAN',"26.04","38.06"],
               ['Share-USUF',"9.25","27.69"],
               ['Share-CFOZ',"10.64","38.21"]
            ]
    dataset = [share(name=name.strip(),value=float(value),roi=float(roi)/100) for name, value, roi in raw_set if float(value)>0]
    
    sort_fct = lambda x : x.roi
    capacity = 40
    shares, cost, roi = branch_and_bound(dataset, capacity, sort_fct)
    print(f'{shares}\ncout: {cost} gain : {roi}')
