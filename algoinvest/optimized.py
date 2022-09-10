from collections import namedtuple

def optimized():
    pass

# methode separation et evaluation Horowitz et sahni
def horowitz_sahni_algo(market, capacity):
    best_solution = []
    current_solution = []
    residual_capacity = capacity
    next_item = ""
    next_weight = ""
    n = 1
    pass

def compute_upper_bound():
    pass

def branch_and_bound(market, capacity):
    node = namedtuple('node',('index', 'gain', 'bound', 'weight'))
    
    market.sort(key=lambda x : x.roi, reverse=True)
    
    queue = []
    dummy_node = node(index=-1, gain=0, bound=0, weight=0)
    next_node = node(index="", gain="", bound="", weight="")
    queue.append(dummy_node)

    max_roi = 0
    index = len(market)
    while queue:
        # sort un noeud de la file
        node_ref=queue[0]
        queue.pop(0)

        # si le 1er noeud_ref est le dummy_node
        # le next_node prend le niveau 0
        if node_ref.index == -1:
            next_node.index = 0
        
        # change de noeud de reference si l'ensemble de la liste 
        # a ete parcouru
        if node_ref.index == index-1:
            continue

        # ajoute le noeud a la serie
        next_node.index = node_ref.index+1
        next_node.weight = node_ref.weight + market[next_node.index].weight
        next_node.gain = node_ref.gain + market[next_node.index].value

        # met a jour le montant max si les conditions sont respecte
        if next_node.weight <= capacity and next_node.gain > max_roi:
            max_roi = next_node.gain
        
        # calcule la valeur maximal possible de la branche
        next_node.bound = bound(next_node, len(market), capacity, market)
        
        # si les gains sont plus important ajout le noeud à la liste 
        if next_node.bound > max_roi:
            queue.append(next_node)
    return max_roi

def bound(node, capacity, market):
    if node.weight >= capacity:
        return 0
    
    bound = node.gain
    index = node.index+1
    total_weight = node.weight

    # parcourd la liste et ajoute chaque noeud qui respect les conditions
    while index <= len(market) and (total_weight + market[index].weight <= capacity):
        total_weight += market[index].weight
        bound += market[index].value
        index+=1

    if index < len(market):
        bound += (capacity - total_weight)*market[index].value/market[index].weight

    return bound 
    

    

if __name__ == '__main__':
    pass