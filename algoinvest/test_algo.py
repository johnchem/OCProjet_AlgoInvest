from pickletools import optimize
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

def test_bruteforce_set_1(dataset_1, control_set_1):
    analysis = brute_force_matrice(dataset_1[:20])
    # shares = analysis["shares"]
    cost = analysis["cost"]
    roi = analysis["roi"]

    assert cost <= control_set_1['cost']
    assert roi >= control_set_1['roi']

def test_bruteforce_set_2(dataset_2, control_set_2):
    shares, cost, roi = brute_force(dataset_2)

    assert all(s in control_set_2 for s in shares if s != "")
    assert cost <= control_set_2['cost']
    assert roi >= control_set_2['roi']

def test_branch_and_bound_set_1(dataset_1, control_set_1):
    shares, cost, roi = optimized(dataset_1)
    
    assert cost <= control_set_1['cost']
    assert roi >= control_set_1['roi']

def test_optimized_set_2(dataset_2, control_set_2):
    shares, cost, roi = optimized(dataset_2)

    assert all(s in control_set_2 for s in shares)
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
        testing_data = [share(name=name.strip(),value=float(value),roi=float(roi)) for name, value, roi in reader if float(value)>0]
    return testing_data



@pytest.fixture
def dataset_1():
    FILE_NAME = DATA_SET_FOLDER/'dataset1_Python+P7.csv'
    
    share = namedtuple('share',('name', 'value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        testing_data = [share(name=name.strip(),value=float(value),roi=float(roi)) for name, value, roi in reader if float(value)>0]
    return testing_data


@pytest.fixture
def dataset_2():
    FILE_NAME = DATA_SET_FOLDER/'dataset2_Python+P7.csv'
    
    share = namedtuple('share',('name', 'value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        control_data = [share(name=name.strip(), value=float(value),roi=float(roi)) for name, value, roi in reader if float(value)>0]
    return control_data


@pytest.fixture
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
    # import sys
    # sys.setrecursionlimit(1000000)
    data_set = dataset_0()
    #print(branch_and_bound(data_set, 500))  
    n = len(data_set)
    capacity = 50
    value = [x.value for x in data_set]
    roi = [x.roi*x.value/100 for x in data_set]
    p_per_weight = [x.roi*x.value/x.value for x in data_set]

    print(branch_and_bound(n, value, roi, capacity, p_per_weight))

    # sort_fct_1 = lambda x : x.roi*x.roi*x.value
    # # knapsack_1 = knapsack_H_S(data_set, 500, sort_fct_1)
    # bag = Knapsack(data_set, 500, sort_fct_1)

    # # sort_fct_2 = lambda x : x.roi*x.value
    # # knapsack_2 = knapsack_H_S(data_set, 500, sort_fct_2)
    
    # upper_bound = opti.UpperBoundhandler()
    # step_forward = opti.StepForwardHandler()
    # best_solution = opti.UpdateSolutionHandler()
    # back_track = opti.BackTrackHandler()
    # upper_bound.set_next(step_forward).set_next(best_solution).set_next(back_track).set_next(step_forward)
    # upper_bound.set_branch(back_track)
    # step_forward.set_branch(upper_bound)
    # step_forward.set_branch_2(step_forward)
    # back_track.set_branch(step_forward)

    # result = upper_bound.handle(bag)
    # print(result)
    # # print(knapsack_1(upper_bound))

    # print(knapsack_2(upper_bound))
    # print(horowitz_sahni_algo(data_set,50))