
import copy
import logging
from memory_profiler import profile

logging.basicConfig(filename='./bruteforce.log', filemode='w', encoding='utf-8', level=logging.DEBUG)

@profile
def brute_force(market):
    investment_list = [{'shares':[], 'cost':0, 'roi':0}]
    for share in market:
        print(f"brute force {share}")
        investment_list = add_share(share, investment_list)
    
    filtered_list = [item for item in investment_list if item["cost"]<500]
    print(*filtered_list, sep='\n')
    return filtered_list[0]

def add_share(share, investment):
    output = []
    for invest in investment:
        choice_1, choice_2 = copy.deepcopy(invest), copy.deepcopy(invest)
        
        choice_1["shares"].append(share.name)
        choice_1["cost"] += float(share.value)
        choice_1["roi"] += float(share.value*share.roi/100)

        choice_2["shares"].append("")
        output.append(choice_1)
        output.append(choice_2)
    return output

class Tree:
    def __init__(self, root = None):
        self.root=root
class Node:
    def __init__(self, v, g=None, d=None):
        self.g, self.d = g, d
        self.v = v

    def __repr__(self):
        return f"{self.v}: ({self.g} / {self.d})"

def structure_arbre(market):
    arbre = Tree(Node("root"))
    previous_rank=[arbre.root]
    for share in market:
        tmp_rank = []
        for node in previous_rank:
            nd, ng = add_leaves(node, share.name, None)
            tmp_rank.append(nd)
            tmp_rank.append(ng)
            print(previous_rank)
        previous_rank = tmp_rank
    return arbre

def generate_matrix(size):
    matrice = [[0]*size]
    for i in range(size):
        matrice.extend(copy.deepcopy(matrice))
        for j in range(len(matrice)//2):
            matrice[j][i] = 1
    print("### final ###")
    return matrice

def add_leaves(node, nd_value, ng_value):
    node.d = Node(nd_value)
    node.g = Node(ng_value)
    return node.d, node.g


if __name__ == '__main__':
    print(*generate_matrix(20), sep="\n")
