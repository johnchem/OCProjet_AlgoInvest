from collections import namedtuple
from bruteforce import brute_force
from optimized import optimized
from pathlib import Path
import csv

def test_bruteforce_set_1():
    DATA_SET_FOLDER = Path("algoinvest/dataset")
    control_set_1 = import_control_set_1(DATA_SET_FOLDER/'control_dataset1.csv')
    testing_set_1 = import_dataset(DATA_SET_FOLDER/'dataset1_Python+P7.csv')
    
def test_bruteforce_set_2():
    DATA_SET_FOLDER = Path("algoinvest/dataset")
    control_set_2 = import_control_set_2(DATA_SET_FOLDER/'control_dataset2.csv')
    testing_set_2 = import_dataset(DATA_SET_FOLDER/'dataset2_Python+P7.csv')

def test_optimized_set_1():
    DATA_SET_FOLDER = Path("algoinvest/dataset")
    control_set_1 = import_control_set_1(DATA_SET_FOLDER/'control_dataset1.csv')
    testing_set_1 = import_dataset(DATA_SET_FOLDER/'dataset1_Python+P7.csv')

def test_optimized_set_2():
    DATA_SET_FOLDER = Path("algoinvest/dataset")
    control_set_2 = import_control_set_2(DATA_SET_FOLDER/'control_dataset2.csv')
    testing_set_2 = import_dataset(DATA_SET_FOLDER/'dataset2_Python+P7.csv')


def import_dataset(fileName):
    share = namedtuple('share',('value', 'roi'))
    with open(fileName, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        control_data = {key:share(value=value,roi=roi) for key, value, roi in reader}
    return control_data


def import_control_set_1(fileName):
    with open(fileName, newline='') as f:
        print('tutu')
        reader = csv.reader(f, delimiter= ',')
        control_data = {key.strip():value.strip() for key, value in reader}
    del control_data['Sienna bought:']
    return control_data


def import_control_set_2(fileName):
    with open(fileName, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        control_data = {key.strip():value.strip() for key, value in reader}
    del control_data['Sienna bought:']
    return control_data


if __name__ == "__main__":
    pass