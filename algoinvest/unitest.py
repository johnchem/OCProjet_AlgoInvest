from bruteforce import brute_force
from optimized import optimized

from pathlib import Path
from collections import namedtuple
import pytest
import csv

#define testing constant
DATA_SET_FOLDER = Path("algoinvest/dataset")

def test_bruteforce_set_1(dataset_1, control_set_1):
    shares, cost, roi = brute_force(dataset_1)

    assert all(share in dataset_1 for share in shares)
    assert cost <= control_set_1['cost']
    assert roi >= control_set_1['roi']


def test_bruteforce_set_2(dataset_2, control_set_2):
    shares, cost, roi = brute_force(dataset_2)

    assert all(share in dataset_2 for share in shares)
    assert cost <= control_set_2['cost']
    assert roi >= control_set_2['roi']

def test_optimized_set_1(dataset_1, control_set_1):
    shares, cost, roi = optimized(dataset_1)
    
    assert all(share in dataset_1 for share in shares)
    assert cost <= control_set_1['cost']
    assert roi >= control_set_1['roi']


def test_optimized_set_2(dataset_2, control_set_2):
    shares, cost, roi = optimized(dataset_2)

    assert all(share in dataset_2 for share in shares)
    assert cost <= control_set_2['cost']
    assert roi >= control_set_2['roi']


"""
define the fixture
"""
@pytest.fixture
def dataset_1():
    FILE_NAME = DATA_SET_FOLDER/'dataset1_Python+P7.csv'
    
    share = namedtuple('share',('value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        control_data = {key:share(value=value,roi=roi) for key, value, roi in reader}
    return control_data


@pytest.fixture
def dataset_2():
    FILE_NAME = DATA_SET_FOLDER/'dataset2_Python+P7.csv'
    
    share = namedtuple('share',('value', 'roi'))
    with open(FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        control_data = {key:share(value=value,roi=roi) for key, value, roi in reader}
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