from bruteforce import brute_force
from optimized import optimized

from pathlib import Path
from collections import namedtuple
import logging
import pytest
import csv

#define testing constant
DATA_SET_FOLDER = Path("algoinvest/dataset")

def test_bruteforce_set_1(dataset_1, control_set_1):
    analysis = brute_force(dataset_1[:20])
    shares = analysis["shares"]
    cost = analysis["cost"]
    roi = analysis["roi"]

    assert all(s in control_set_1 for s in shares)
    assert cost <= control_set_1['cost']
    assert roi >= control_set_1['roi']


def test_bruteforce_set_2(dataset_2, control_set_2):
    shares, cost, roi = brute_force(dataset_2)

    assert all(s in control_set_2 for s in shares if s != "")
    assert cost <= control_set_2['cost']
    assert roi >= control_set_2['roi']

def test_optimized_set_1(dataset_1, control_set_1):
    shares, cost, roi = optimized(dataset_1)
    
    assert all(s in control_set_1 for s in shares)
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
    output = dataset_1()
    print(*dataset_1().items(), sep="\n")
    