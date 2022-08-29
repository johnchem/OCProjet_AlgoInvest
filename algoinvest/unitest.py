from collections import namedtuple
from pathlib import Path
import csv

def unitest_testing_set_1(function):
    pass

def unitest_testing_set_2(function):
    pass

def import_dataset(fileName):
    share = namedtuple('share',('value', 'roi'))
    with open(fileName, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        next(reader) #skip the 1st line
        controlData = {key:share(value=value,roi=roi) for key, value, roi in reader}
    return controlData


def import_control_set_1(fileName):
    with open(fileName, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        controlData = {key.strip():value.strip() for key, value in reader}
    del controlData['Sienna bought:']
    return controlData


def import_control_set_2(fileName):
    with open(fileName, newline='') as f:
        reader = csv.reader(f, delimiter= ',')
        controlData = {key.strip():value.strip() for key, value in reader}
    del controlData['Sienna bought:']
    return controlData


if __name__ == "__main__":
    DATASETFOLDER = Path("algoinvest/dataset")
    controlSet1 = import_control_set_1(DATASETFOLDER/'control_dataset1.csv')
    controlSet2 = import_control_set_2(DATASETFOLDER/'control_dataset2.csv')
    
    testingSet1 = import_dataset(DATASETFOLDER/'dataset1_Python+P7.csv')
    testingSet2 = import_dataset(DATASETFOLDER/'dataset2_Python+P7.csv')