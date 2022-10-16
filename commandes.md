# initialisation
poetry shell

# bruteforce with dataset 0
pytest algoinvest\test_algo.py -k test_bruteforce -s -vv

# branch and bound with dataset 1
pytest algoinvest\test_algo.py -k test_branch_and_bound_set_1 -s -vv

# branch and bound with dataset 2
pytest algoinvest\test_algo.py -k test_branch_and_bound_set_2 -s -vv

# branch and bound speed test
pytest algoinvest\test_algo.py -k "test_time" -s -vv

# branch and bound memory test
pytest algoinvest\test_algo.py -k "test_memory" -s -vv
