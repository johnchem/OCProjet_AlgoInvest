
import copy
from tqdm import tqdm, trange

def generate_matrix(size):
    matrice = [[0]*size]
    for i in trange(size):
        matrice.extend(copy.deepcopy(matrice))
        for j in range(len(matrice)//2):
            matrice[j][i] = 1
    return matrice

def brute_force_matrice(market, capacity):
    matrice = generate_matrix(len(market))
    liste_action = market
    roi_max = 0
    best_investment = []
    for row in tqdm(matrice):
        investment = [action for buy, action in zip(row, liste_action) if buy == 1]
        cost = sum([int(price) for action, price, roi in investment])
        if cost<capacity:
            total_roi = sum(roi*price for action, price, roi in investment)
            if total_roi>roi_max:
                roi_max = total_roi
                total_cost = cost
                best_investment = [action for action in investment]
    print(f"benefice maximal {roi_max}")
    print(f"cout de l'achat {total_cost}")
    return best_investment, round(total_cost, 2), round(roi_max, 2)

if __name__ == '__main__':
    pass