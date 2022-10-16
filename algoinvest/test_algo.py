import random
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
    
    shares_list = [(x.name, x.value, x.roi) for x in shares]
    output_string = f'actions \n {" ".join(shares_list)} \n coût {cost} gain total {roi}'
    print(output_string)

    assert cost <= capacity
    assert roi >= float(control_set_1['roi'])


def test_branch_and_bound_set_2(dataset_2, control_set_2, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    shares, cost, roi = benchmark(branch_and_bound, dataset_2, capacity, sort_fct)
    
    shares_list = [(x.name, x.value, x.roi) for x in shares]
    output_string = f'actions \n {" ".join(shares_list)} \n coût {cost} gain total {roi}'
    print(output_string)

    assert cost <= capacity
    assert roi >= float(control_set_2['roi'])


"""
time benchmark
"""

def test_time_bb_1(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    sample = 250
    dataset = random.sample(dataset_1, sample)
    shares, cost, roi = benchmark(branch_and_bound, dataset, capacity, sort_fct)
    
    assert cost <= capacity
    

def test_time_bb_2(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    sample = 500
    dataset = random.sample(dataset_1, sample)
    shares, cost, roi = benchmark(branch_and_bound, dataset, capacity, sort_fct)
   
    assert cost <= capacity
    

def test_time_bb_3(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    sample = 750
    dataset = random.sample(dataset_1, sample)
    shares, cost, roi = benchmark(branch_and_bound, dataset, capacity, sort_fct)
    
    assert cost <= capacity
    

def test_time_bb_4(dataset_1, benchmark):
    sort_fct = lambda x : x.roi
    capacity = 500
    shares, cost, roi = benchmark(branch_and_bound, dataset_1, capacity, sort_fct)
    
    assert cost <= capacity
    

"""
test memory consumption
"""


def test_memory_bb_1(dataset_1):
    from memory_profiler import memory_usage
    sort_fct = lambda x : x.roi
    capacity = 500
    sample = 250
    dataset = random.sample(dataset_1, sample)
    mem_usage = memory_usage((branch_and_bound, (dataset, capacity, sort_fct,)))
    print(max(mem_usage))


def test_memory_bb_2(dataset_1):
    from memory_profiler import memory_usage
    sort_fct = lambda x : x.roi
    capacity = 500
    sample = 500
    dataset = random.sample(dataset_1, sample)
    mem_usage = memory_usage((branch_and_bound, (dataset, capacity, sort_fct,)))
    print(max(mem_usage))


def test_memory_bb_3(dataset_1):
    from memory_profiler import memory_usage
    sort_fct = lambda x : x.roi
    capacity = 500
    sample = 750
    dataset = random.sample(dataset_1, sample)
    mem_usage = memory_usage((branch_and_bound, (dataset, capacity, sort_fct,)))
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
    pass
