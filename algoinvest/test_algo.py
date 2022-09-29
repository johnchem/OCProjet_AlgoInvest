from pickletools import optimize
from time import time
from algoinvest.bruteforce import brute_force_matrice
from algoinvest.optimized import knapsack_H_S, Knapsack
from algoinvest.branch_and_bound import branch_and_bound
from bruteforce import brute_force
import algoinvest.optimized as opti

from pathlib import Path
from collections import namedtuple
import pytest
import csv

#define testing constant
DATA_SET_FOLDER = Path("algoinvest/dataset")

def test_bruteforce(dataset_0, control_set_1):
    analysis = brute_force_matrice(dataset_0)
    # shares = analysis["shares"]
    cost = analysis["cost"]
    roi = analysis["roi"]

    assert cost <= control_set_1['cost']
    assert roi >= control_set_1['roi']

def test_branch_and_bound_set_1(dataset_1, control_set_1):
    sort_fct_1 = lambda x : x.roi
    dataset_1.sort(key=sort_fct_1, reverse=True)
    n = len(dataset_1)
    capacity = 500
    value = [x.value for x in dataset_1]
    roi = [x.roi*x.value for x in dataset_1]
    p_per_weight = [x.roi for x in dataset_1]
        
    result = branch_and_bound(n, roi, value, capacity, p_per_weight)
    print([dataset_1[x].name for x in result])

    shares, cost, roi = branch_and_bound(dataset_1)
    
    assert cost <= control_set_1['cost']
    assert roi >= control_set_1['roi']

def test_branch_and_bound_set_2(dataset_2, control_set_2):
    sort_fct = lambda x : x.roi
    dataset_2.sort(key=sort_fct, reverse=True)
    n = len(dataset_2)
    capacity = 500
    value = [x.value for x in dataset_2]
    roi = [x.roi*x.value for x in dataset_2]
    p_per_weight = [x.roi for x in dataset_2]
        
    result = branch_and_bound(n, roi, value, capacity, p_per_weight)
    print([dataset_2[x].name for x in result])

    shares, cost, roi = branch_and_bound(dataset_1)
    
    assert cost <= control_set_2['cost']
    assert roi >= control_set_2['roi']


"""
define the fixture
"""

def dataset_0():
    FILE_NAME = DATA_SET_FOLDER/'dataset_0.csv'
    
    share = namedtuple('share',('name', 'value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        testing_data = [share(name=name.strip(),value=float(value),roi=float(roi)/100) for name, value, roi in reader if float(value)>0]
    return testing_data

def dataset_0_bis():
    FILE_NAME = DATA_SET_FOLDER/'dataset_0_bis.csv'
    
    share = namedtuple('share',('name', 'value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        testing_data = [share(name=name.strip(),value=float(value),roi=float(roi)/100) for name, value, roi in reader if float(value)>0]
    return testing_data



# @pytest.fixture
def dataset_1():
    FILE_NAME = DATA_SET_FOLDER/'dataset1_Python+P7.csv'
    
    share = namedtuple('share',('name', 'value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        testing_data = [share(name=name.strip(),value=float(value),roi=float(roi)/100) for name, value, roi in reader if float(value)>0]
    return testing_data

@pytest.fixture
def dataset_2():
    FILE_NAME = DATA_SET_FOLDER/'dataset2_Python+P7.csv'
    
    share = namedtuple('share',('name', 'value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        control_data = [share(name=name.strip(), value=float(value),roi=float(roi)/100) for name, value, roi in reader if float(value)>0]
    return control_data


# @pytest.fixture
def control_set_1():
    FILE_NAME = DATA_SET_FOLDER/'control_dataset1.csv'

    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        control_data = {key.strip():value.strip() for key, value in reader}
    del control_data['Sienna bought:']
    control_data['cost'] = control_data.pop('Total cost:')
    control_data['roi'] = control_data.pop('Total return:')
    return control_data

@pytest.fixture
def control_set_2():
    FILE_NAME = DATA_SET_FOLDER/'control_dataset2.csv'

    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        control_data = {key.strip():value.strip() for key, value in reader}
    del control_data['Sienna bought:']
    control_data['cost'] = control_data.pop('Total cost:')
    control_data['roi'] = control_data.pop('Profit:')
    return control_data

if __name__ == "__main__":
    import timeit
    from memory_profiler import memory_usage
    import sys
    sys.setrecursionlimit(10000)
    data_set = dataset_0()
    #print(branch_and_bound(data_set, 500)) 
    def test_bruteforce_5():
        brute_force_matrice(data_set[:5])

    def test_bruteforce_10():
        brute_force_matrice(data_set[:10])

    def test_bruteforce_15():
        brute_force_matrice(data_set[:15])

    def test_bruteforce_20():
        brute_force_matrice(data_set)

    # print(timeit.repeat(test_bruteforce_5, repeat=3, number=1))
    # print(timeit.repeat(test_bruteforce_10, repeat = 3, number=1))
    # print(timeit.repeat(test_bruteforce_15, repeat=3, number=1))
    # print(timeit.repeat(test_bruteforce_20, repeat=3, number=1))

    
    mem_usage_5 = memory_usage(test_bruteforce_5)
    mem_usage_10 = memory_usage(test_bruteforce_10)
    mem_usage_15 = memory_usage(test_bruteforce_15)
    mem_usage_20 = memory_usage(test_bruteforce_20)

    print([max(mem_usage_5), max(mem_usage_10), max(mem_usage_15), max(mem_usage_20)], sep='\n')

    def test_bb():
        ds = list(data_set)
        sort_fct_1 = lambda x : x.roi
        ds.sort(key=sort_fct_1, reverse=True)
        print(*ds, sep='\n')
        n = len(ds)
        capacity = 500
        value = [x.value for x in ds]
        roi = [x.roi*x.value for x in ds]
        p_per_weight = [x.roi for x in ds]
        
        print("\n_______ branch & bound _______\n")
        result = branch_and_bound(n, roi, value, capacity, p_per_weight)
        print([ds[x].name for x in result])
    # print(timeit.timeit(test_bb, number=1))

    def test_HS_bb():
        sort_fct_1 = lambda x : x.roi
        knapsack_1 = knapsack_H_S(data_set, 500, sort_fct_1)
    
        upper_bound = opti.UpperBoundhandler()
        step_forward = opti.StepForwardHandler()
        best_solution = opti.UpdateSolutionHandler()
        back_track = opti.BackTrackHandler()
        upper_bound.set_next(step_forward).set_next(best_solution).set_next(back_track).set_next(step_forward)
        upper_bound.set_branch(back_track)
        step_forward.set_branch(upper_bound)
        step_forward.set_branch_2(step_forward)
        back_track.set_branch(step_forward)

        print("\n_______ H&S branch & bound _______\n")
        print(f'start {knapsack_1}')
        print(knapsack_1(upper_bound))
    # print(timeit.timeit(test_HS_bb, number=1))
