from collections import namedtuple
from math import floor
import copy

def optimized():
    pass

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