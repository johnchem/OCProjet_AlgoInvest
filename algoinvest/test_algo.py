from algoinvest.bruteforce import brute_force_matrice
from algoinvest.optimized import branch_and_bound
import time

from pathlib import Path
from collections import namedtuple
import pytest
import csv

#define testing constant
DATA_SET_FOLDER = Path("algoinvest/dataset")


"""
functional tests
"""

def test_bruteforce(dataset_0):
    capacity = 500
    shares, cost, roi = brute_force_matrice(dataset_0, capacity)
    
    shares_list = [x.name for x in shares]
    output_string = f'actions \n {" ".join(shares_list)} \n coût {cost} gain total {roi}'
    print(output_string)

    assert cost <= capacity


def test_branch_and_bound_set_1(dataset_1, control_set_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    shares, cost, roi = benchmark(branch_and_bound, dataset_1, capacity, sort_fct)
    
    shares_list = [x.name for x in shares]
    output_string = f'actions {shares_list} \n coût {cost} gain total {roi}'
    print(output_string)

    assert cost <= capacity
    assert roi >= float(control_set_1['roi'])


def test_branch_and_bound_set_2(dataset_2, control_set_2, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    shares, cost, roi = benchmark(branch_and_bound, dataset_2, capacity, sort_fct)
    
    shares_list = [x.name for x in shares]
    output_string = f'actions {shares_list} \n coût {cost} gain total {roi}'
    print(output_string)

    assert cost <= capacity
    assert roi >= float(control_set_2['roi'])


"""
time benchmark
"""

def test_time_bb_1(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    benchmark(branch_and_bound, dataset_1[:250], capacity, sort_fct)


def test_time_bb_2(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    benchmark(branch_and_bound, dataset_1[:500], capacity, sort_fct)
    

def test_time_bb_3(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    benchmark(branch_and_bound, dataset_1[:750], capacity, sort_fct)
    

def test_time_bb_4(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    benchmark(branch_and_bound, dataset_1, capacity, sort_fct)


"""
test memory consumption
"""


def test_memory_bb_1(dataset_1):
    from memory_profiler import memory_usage
    sort_fct = lambda x : x.roi
    capacity = 500
    mem_usage = memory_usage((branch_and_bound, (dataset_1[:250], capacity, sort_fct,)))
    print(max(mem_usage))


def test_memory_bb_2(dataset_1):
    from memory_profiler import memory_usage
    sort_fct = lambda x : x.roi
    capacity = 500
    mem_usage = memory_usage((branch_and_bound, (dataset_1[:500], capacity, sort_fct,)))
    print(max(mem_usage))


def test_memory_bb_3(dataset_1):
    from memory_profiler import memory_usage
    sort_fct = lambda x : x.roi
    capacity = 500
    mem_usage = memory_usage((branch_and_bound, (dataset_1[:750], capacity, sort_fct,)))
    print(max(mem_usage))


def test_memory_bb_4(dataset_1):
    from memory_profiler import memory_usage
    sort_fct = lambda x : x.roi
    capacity = 500
    mem_usage = memory_usage((branch_and_bound, (dataset_1, capacity, sort_fct,)))
    print(max(mem_usage))


"""
define the fixture
"""
@pytest.fixture
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


@pytest.fixture
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
