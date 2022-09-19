from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import floor
import copy

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
            critical_point_balance = knap.items[critical_point].roi*knap.items[critical_point].value/knap.items[critical_point].value
            upper_bound = (gain_at_critical_point + 
                                floor((knap.res_capacity - weight_at_critical_point)*
                                       critical_point_balance)
                          )
        node({'current exploration':knap.current_sol["path"],
                     'critical point':critical_point,
                     'upper bound':upper_bound})
        # print(f'critical point {critical_point}')
        # print(f'upper bound {upper_bound}')
        
        if knap.best_sol['gain'] >= knap.current_sol['gain'] + upper_bound:
            return self._branch_handler.handler(knap)
        else:
            return self._next_handler.handler(knap)


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
        while knap.items[knap.i].value <= knap.residual_cap:
            knap.residual_cap -= knap.items[knap.i].value
            knap.residual_cap['gain'] += knap.items[knap.i].roi*knap.items[knap.i].value
            knap.residual_cap['path'][knap.i]=1
            knap.i += 1

            if knap.i >= knap.n: 
                break
            node({'current exploration':knap.current_sol["path"], 
                         'residual':knap.res_capacity}
                       )
            
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
                return self._branch_handler_2(knap)
            # when all the items have been evaluated => update_best_solution 
            return self._next_handler(knap)


class UpdateSolutionHandler(AbstractHandler):
    def handle(self, knap):
        node({'current exploration':knap.current_sol["path"], 
                     'current gain':round(knap.current_sol["gain"])}
                    )
        # print(f'current gain {round(current_solution["gain"])}')
        if knap.current_sol ['gain'] > knap.best_sol['gain']:
            knap.best_sol = copy.deepcopy(knap.current_sol)
        
        # reinitialisation de l'index
        knap.i = knap.n-1

        # si le dernier objet est mis dans le sac, mise a jour de la valeur 
        # et passage dans path[-1] == 0 pour permettre le back-tracking
        if knap.current_sol['path'][-1]:
            knap.res_capacity += knap.items[-1].value
            knap.current_sol['gain'] -= knap.items[-1].roi*knap.items[-1].value
            knap.current_sol['path'][-1] = 0
        return self._next_handler.handler(knap)


class BackTrackHandler(AbstractHandler):
    def handle(self, knap):
        backtrack_index = max([i for i,x in enumerate(knap.current_sol['path']) if x==1])
        if not backtrack_index:
            return knap.best_sol
        
        # take back the last items put in the bag
        knap.res_capacity += knap.items[backtrack_index].value
        knap.current_sol['gain'] -= knap.items[backtrack_index].roi*knap.items[backtrack_index].value
        # set the node to explore with a value None
        knap.current_sol['path'][backtrack_index:]=[None]*(len(knap.current_sol["path"])-backtrack_index)
        # force the current node to 0
        knap.current_sol['path'][backtrack_index]=0
        knap.i = backtrack_index + 1
        return self._next_handler.handler(knap)


@dataclass
class Knapsack:
    node_i = 0
    i = 0
    
    def __init__(self, items, capacity, sort_fct=None):
        self._items = items
        self.items = items
        self.items.sort(key=sort_fct, reverse = True)
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

def create_node():
    def print_node(infos):
        print(f'\nnode {node_nb}')
        node_nb += 1
        for name, info in infos.items():
            print(f'{name} {info}')
        return
    node_nb = 0
    return print_node

node = create_node()


# methode separation et evaluation Horowitz et sahni
def horowitz_sahni_algo(market, capacity):
    def initialise():
        best_solution = {'gain':0 ,'path':[None]*nb_items}
        current_solution = {'gain':0 ,'path':[None]*nb_items}
        residual_capacity = capacity
        index = 0
        return best_solution, current_solution, residual_capacity, index
    
    def get_critical_point():
        critical_point = index
        critical_value = 0
        
        search_critical = True
        while search_critical:
            if critical_point >= nb_items:
                search_critical = False
                continue
            if critical_value + market[critical_point].value > residual_capacity:
                search_critical = False
                continue
            critical_value += market[critical_point].value
            critical_point += 1
            
        return critical_point
    
    def get_upper_bound():
        critical_point = get_critical_point()
        # gestion du cas où tous les items restant peuvent être mis dans le sac
        if critical_point >= nb_items:
            upper_bound = floor(sum([market[j].roi*market[j].value for j in range(index, nb_items)]))

        else:
            # cas par defaut et cas ou index = critical_point['index']
            gain_at_critical_point = sum([market[j].roi*market[j].value for j in range(index, critical_point)]) 
            weight_at_critical_point = sum([market[j].value for j in range(index, critical_point)])
            critical_point_balance = market[critical_point].roi*market[critical_point].value/market[critical_point].value
            upper_bound = (gain_at_critical_point + 
                                floor((residual_capacity - weight_at_critical_point)*
                                       critical_point_balance)
                          )
        create_node({'current exploration':current_solution["path"],
                     'critical point':critical_point,
                     'upper bound':upper_bound})
        # print(f'critical point {critical_point}')
        # print(f'upper bound {upper_bound}')
        
        if best_solution['gain'] >= current_solution['gain'] + upper_bound:
            return start_backtrack()
        return start_forward()
    
    def start_forward():
        nonlocal residual_capacity
        nonlocal current_solution
        nonlocal index
        # ajout tous les objets rentrant dans le sac
        while market[index].value <= residual_capacity:
            residual_capacity -= market[index].value
            current_solution['gain'] += market[index].roi*market[index].value
            current_solution['path'][index]=1
            index += 1

            if index >= nb_items: 
                break
            create_node({'current exploration':current_solution["path"], 
                         'residual':residual_capacity}
                        )
        
        # reject l'object si il ne rentre pas dans le sac
        if index <= nb_items-1:
            current_solution['path'][index] = 0
            index += 1
        
        # si l'object ne rentre dans le sac : 
        # - evaluation of the node with upper_bound
        if index <= nb_items-1:
            return get_upper_bound()
        # - add or reject the item through the start_forward evaluation
        if index == nb_items-1:
            return start_forward()
        # when all the items have been evaluated => update_best_solution 
        return update_best_solution()

    def update_best_solution():
        nonlocal residual_capacity
        nonlocal current_solution
        nonlocal best_solution
        nonlocal index

        create_node({'current exploration':current_solution["path"], 
                     'current gain':round(current_solution["gain"])}
                    )
        # print(f'current gain {round(current_solution["gain"])}')
        if current_solution ['gain'] > best_solution['gain']:
            best_solution = copy.deepcopy(current_solution)
        
        # reinitialisation de l'index
        index = nb_items-1

        # si le dernier objet est mis dans le sac, mise a jour de la valeur 
        # et passage dans path[-1] == 0 pour permettre le back-tracking
        if current_solution['path'][-1]:
            residual_capacity += market[-1].value
            current_solution['gain'] -= market[-1].roi*market[-1].value
            current_solution['path'][-1] = 0
        return start_backtrack()
        
    def start_backtrack():
        nonlocal current_solution
        nonlocal residual_capacity
        nonlocal index

        backtrack_index = max([i for i,x in enumerate(current_solution['path']) if x==1])
        if not backtrack_index:
            return None
        
        # take back the last items put in the bag
        residual_capacity += market[backtrack_index].value
        current_solution['gain'] -= market[backtrack_index].roi*market[backtrack_index].value
        # set the node to explore with a value None
        current_solution['path'][backtrack_index:]=[None]*(len(current_solution["path"])-backtrack_index)
        # force the current node to 0
        current_solution['path'][backtrack_index]=0
        index = backtrack_index + 1
        return get_upper_bound()

    def create_node(infos):
        nonlocal node_i
        
        print(f'\nnode {node_i}')
        node_i += 1
        for name, info in infos.items():
            print(f'{name} {info}')

    node_i = 0
    nb_items = len(market)
            
    best_solution, current_solution, residual_capacity, index = initialise()
    # market.sort(key=lambda x : x.roi*x.value, reverse=True)
    
    get_upper_bound()
    
    return best_solution
        
def branch_and_bound(market, capacity):
    market.sort(key=lambda x : x.roi, reverse=True)
    
    queue = []
    dummy_node = {"index":-1, "gain":0, "bound":0, "weight":0}
    next_node = {"index":"", "gain":"", "bound": "", "weight":""}
    queue.append(dummy_node)

    max_roi = 0
    index = len(market)
    while queue:
        # sort un noeud de la file
        node_ref=queue[0]
        queue.pop(0)
        print(f"index : {index}")
        print(f'queue begin: {queue}')

        # si le 1er noeud_ref est le dummy_node
        # le next_node prend le niveau 0
        if node_ref["index"] == -1:
            next_node["index"] = 0
        
        # change de noeud de reference si l'ensemble de la liste 
        # a ete parcouru
        if node_ref["index"] == index-1:
            continue

        # ajoute le noeud a la serie
        next_node["index"] = node_ref["index"]+1
        next_node["weight"] = node_ref["weight"] + market[next_node["index"]].value
        next_node["gain"] = node_ref["gain"] + market[next_node["index"]].roi

        # met a jour le montant max si les conditions sont respecte
        if next_node["weight"] <= capacity and next_node["gain"] > max_roi:
            max_roi = next_node["gain"]
        
        # calcule la valeur maximal possible de la branche
        next_node["bound"] = bound(next_node, capacity, market)
        
        # si les gains sont plus important ajout le noeud à la liste 
        if next_node["bound"] > max_roi:
            queue.append(next_node)
        print(f'queue end {queue}')
    return max_roi

def bound(node, capacity, market):
    if node["weight"] >= capacity:
        return 0
    
    bound = node["gain"]
    index = node["index"]+1
    total_weight = node["weight"]

    # parcourd la liste et ajoute chaque noeud qui respect les conditions
    while index <= len(market) and (total_weight + market[index].value <= capacity):
        total_weight += market[index].value
        bound += market[index].roi
        index+=1

    if index < len(market):
        bound += (capacity - total_weight)*market[index].roi/market[index].value

    return bound 
    
if __name__ == '__main__':
    pass