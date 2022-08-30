
from collections import namedtuple
import copy
from email.policy import default

def brute_force(market):
    list_investment = [{'shares':[], 'cost':0, 'roi':0}]
    for share in market:
        list_investment = add_share(share, list_investment)
    return list_investment

def add_share(share, investment):
    output = []
    for invest in investment:
        choice_1, choice_2 = copy.deepcopy(invest), copy.deepcopy(invest)
        
        choice_1["shares"].append(share[0])
        choice_1["cost"] += int(share[1])
        choice_1["roi"] += round(float(share[1]*share[2]/100), 2)

        choice_2["shares"].append("")
        output.append(choice_1)
        output.append(choice_2)
    return output

if __name__ == '__main__':
    test = [['A',1, 1], ['B',1, 1], ['C',1, 1], ['D',1, 1], ['E',1, 1], ['F',1, 1]]
    test_output = brute_force(test)
    print(*test_output, sep="\n")
