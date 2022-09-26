from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import floor
import copy

def create_node():
    node_nb = 0
    def print_node(infos):
        print(f'\nnode {node_nb}')
        node_nb += 1
        for name, info in infos.items():
            print(f'{name} {info}')
    return print_node

node = create_node()

class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass
    
    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    _next_handler = None
    _branch_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def set_branch(self, handler):
        self._branch_handler = handler
        return None

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class UpperBoundhandler(AbstractHandler):
    def get_critical_point(self, items, nb_items, residual_capacity, index):
        critical_point = index
        critical_value = 0

        search_critical = True
        while search_critical:
            if critical_point >= nb_items:
                search_critical = False
                continue
            if critical_value + items[critical_point].value > residual_capacity:
                search_critical = False
                continue
            critical_value += items[critical_point].value
            critical_point += 1
        # print(f'critical point {critical_point}')
        return critical_point
    
    def handle(self, knap):
        critical_point = self.get_critical_point(knap.items, knap.n, knap.res_capacity, knap.i)
        # gestion du cas où tous les items restant peuvent être mis dans le sac
        if critical_point >= knap.n:
            upper_bound = floor(sum([knap.items[j].roi*knap.items[j].value for j in range(knap.i, knap.n)]))

        else:
            # cas par defaut et cas ou index = critical_point['index']
            gain_at_critical_point = sum([knap.items[j].roi*knap.items[j].value for j in range(knap.i, critical_point)]) 
            weight_at_critical_point = sum([knap.items[j].value for j in range(knap.i, critical_point)])
            critical_point_balance = knap.items[critical_point].roi
            upper_bound = (gain_at_critical_point + 
                                floor((knap.res_capacity - weight_at_critical_point)*
                                       critical_point_balance)
                          )
        # node({'current exploration':knap.current_sol["path"],
        #              'critical point':critical_point,
        #              'upper bound':upper_bound})

        # print(f'critical point {critical_point}')
        # print(f'upper bound {upper_bound}')
        if knap.best_sol['gain'] >= knap.current_sol['gain'] + upper_bound:
            # print(f'stop exploration {knap.current_sol["path"]}')
            return self._branch_handler.handle(knap)
        else:
            return self._next_handler.handle(knap)


class StepForwardHandler(AbstractHandler):
    '''
    next_handler : best solution
    branch_solution : upper_bound
    branch_solution_2 : step_forward
    '''
    _branch_handler_2 = None

    def set_branch_2(self, handler):
        self._branch_handler_2 = handler
        return None

    def handle(self, knap):
        while knap.items[knap.i].value <= knap.res_capacity:
            knap.res_capacity -= knap.items[knap.i].value
            knap.current_sol['gain'] += knap.items[knap.i].roi*knap.items[knap.i].value
            knap.current_sol['path'][knap.i]=1
            knap.i += 1

            if knap.i >= knap.n: 
                break
            # print(f'current exploration {knap.current_sol["path"]}')
            # print(f'residual {knap.res_capacity}')
            
        # reject l'object si il ne rentre pas dans le sac
        if knap.i <= knap.n-1:
            knap.current_sol['path'][knap.i] = 0
            knap.i += 1
            
        # si l'object ne rentre dans le sac : 
        # - evaluation of the node with upper_bound
        if knap.i <= knap.n-1:
            return self._branch_handler.handle(knap)
        # - add or reject the item through the start_forward evaluation
        if knap.i == knap.n-1:
            return self._branch_handler_2.handle(knap)
        # when all the items have been evaluated => update_best_solution 
        return self._next_handler.handle(knap)


class UpdateSolutionHandler(AbstractHandler):
    def handle(self, knap):
        # node({'current exploration':knap.current_sol["path"], 
        #              'current gain':round(knap.current_sol["gain"])}
        #             )
        # print(f'current gain {round(current_solution["gain"])}')
        if knap.current_sol['gain'] > knap.best_sol['gain']:
            knap.best_sol = copy.deepcopy(knap.current_sol)
            # print(f'nouvelle solution {knap.best_sol["gain"]} {knap.best_sol["path"]}')
        # else:
            # print(f'solution alternative {knap.current_sol["gain"]} {knap.current_sol["path"]}')
        # reinitialisation de l'index
        knap.i = knap.n-1

        # si le dernier objet est mis dans le sac, mise a jour de la valeur 
        # et passage dans path[-1] == 0 pour permettre le back-tracking
        if knap.current_sol['path'][-1]:
            knap.res_capacity += knap.items[-1].value
            knap.current_sol['gain'] -= knap.items[-1].roi*knap.items[-1].value
            knap.current_sol['path'][-1] = 0
        return self._next_handler.handle(knap)


class BackTrackHandler(AbstractHandler):
    def handle(self, knap):
        backtrack_index = max([i for i,x in enumerate(knap.current_sol['path']) if x==1])
        if not backtrack_index:
            return knap.best_sol
        
        # print(f'backtrack_index {backtrack_index}')
        # print(f'path {knap.current_sol["path"]}')
        
        # take back the last items put in the bag
        knap.res_capacity += knap.items[backtrack_index].value
        knap.current_sol['gain'] -= knap.items[backtrack_index].roi*knap.items[backtrack_index].value
        # set the node to explore with a value None
        knap.current_sol['path'][backtrack_index:]=[None]*(len(knap.current_sol["path"])-backtrack_index)
        # force the current node to 0
        knap.current_sol['path'][backtrack_index]=0
        knap.i = backtrack_index + 1
        return self._next_handler.handle(knap)


@dataclass
class Knapsack:
    node_i = 0
    i = 0
    
    def __init__(self, items, capacity, sort_fct=None):
        self._items = items
        self.items = list(items)
        self.items.sort(key=sort_fct, reverse = True)
        # print(*items, sep="\n")
        # print(" ")
        # print(*self.items, sep="\n")
        self.n = len(items)

        self.best_sol = {'gain':0 ,'path':[None]*self.n}
        self.current_sol = {'gain':0 ,'path':[None]*self.n}
        self.res_capacity = capacity
        

def knapsack_H_S(items, capacity, sort_fct):
    def solve_knapsack(handler):
        result = handler.handle(knapsack)
        return result
    knapsack = Knapsack(items, capacity, sort_fct)
    return solve_knapsack


    
if __name__ == '__main__':
    pass