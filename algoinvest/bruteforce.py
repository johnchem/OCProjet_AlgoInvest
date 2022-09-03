
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

if __name__ == '__main__':
    logging.debug('putain de fichier')