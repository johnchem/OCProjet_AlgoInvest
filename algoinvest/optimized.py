from collections import namedtuple
from math import floor

def optimized():
    pass

# methode separation et evaluation Horowitz et sahni
def horowitz_sahni_algo(market, capacity):
    def initialise():
        best_solution = {'gain':0 ,'path':[None]*len(market)}
        current_solution = {'gain':0 ,'path':[None]*len(market)}
        residual_capacity = capacity
        index = 0
        return best_solution, current_solution, residual_capacity, index
    
    def get_critical_point():
        critical_point = {'index':index-1, 'value':0}
        while critical_point['value'] < residual_capacity:
            critical_point['index'] += 1
            if critical_point['index'] >= len(market):break
            critical_point['value'] += market[critical_point['index']].value
        return critical_point
    
    def get_upper_bound():
        nonlocal node_i

        critical_point = get_critical_point()
        if critical_point['index'] > len(market)-1:
            upper_bound = sum([market[j].roi*market[j].value for j in range(index, critical_point['index']+1)])

        else:
            gain_at_critical_point = sum([market[j].roi*market[j].value for j in range(index, critical_point['index'])]) 
            weight_at_critical_point = sum([market[j].value for j in range(index, critical_point['index'])])
            critical_point_balance = market[critical_point['index']].roi*market[critical_point['index']].value/market[critical_point['index']].value
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
            start_backtrack()
            return
        start_forward()
        return

    def update_best_solution():
        nonlocal residual_capacity
        nonlocal current_solution
        nonlocal best_solution
        nonlocal index
        nonlocal node_i

        create_node({'current exploration':current_solution["path"], 
                     'current gain':round(current_solution["gain"])}
                    )
        # print(f'current gain {round(current_solution["gain"])}')
        if current_solution ['gain'] > best_solution['gain']:
            best_solution = current_solution.copy()
        
        # reinitialisation de l'index
        index = len(market)-1

        # si le dernier objet est mis dans le sac, mise a jour de la valeur 
        # et passage dans path[-1] == 0 pour permettre le back-tracking
        if current_solution['path'][-1]:
            residual_capacity += market[-1].value
            current_solution['gain'] -= market[-1].roi*market[-1].value
            current_solution['path'][-1] = 0
        start_backtrack()
        return

    def start_forward():
        nonlocal node_i
        nonlocal residual_capacity
        nonlocal current_solution
        nonlocal index
        while market[index].value <= residual_capacity:
            residual_capacity -= market[index].value
            current_solution['gain'] += market[index].roi*market[index].value
            current_solution['path'][index]=1

            create_node({'current exploration':current_solution["path"], 
                         'residual':residual_capacity}
                        )

            index += 1
            if index >= len(market): 
                break
        if index <= len(market)-1:
            current_solution['path'][index] = 0
            index += 1
        if index < len(market)-1:
            get_upper_bound()
            return
        if index == len(market)-1:
            start_forward()
            return
        update_best_solution()
        return 

    
    def start_backtrack():
        nonlocal current_solution
        nonlocal residual_capacity
        nonlocal index

        backtrack_index = max([i for i,x in enumerate(current_solution['path']) if x==1])
        if not backtrack_index:
            return None
        
        residual_capacity += market[backtrack_index].value
        current_solution['gain'] -= market[backtrack_index].roi*market[backtrack_index].value
        # set the node to explore with a value None
        current_solution['path'][backtrack_index:]=[None]*(len(current_solution["path"])-backtrack_index)
        # force the current node to 0
        current_solution['path'][backtrack_index]=0
        index = backtrack_index + 1
        get_upper_bound()
        return

    def create_node(infos):
        nonlocal node_i
        
        print(f'\nnode {node_i}')
        node_i += 1
        for name, info in infos.items():
            print(f'{name} {info}')

    node_i = 0
            
    best_solution, current_solution, residual_capacity, index = initialise()
    # market.sort(key=lambda x : x.roi*x.value, reverse=True)
    
    get_upper_bound()
    start_forward()
    update_best_solution()
    start_backtrack()
    
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