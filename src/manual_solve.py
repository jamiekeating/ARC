#!/usr/bin/python

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.
def solve_7fe24cdd(x):
    top_left = x
    bottom_left = np.array(list(reversed(list(zip(*top_left)))))
    bottom_right = np.array(list(reversed(list(zip(*bottom_left)))))
    top_right = np.array(list(reversed(list(zip(*bottom_right)))))
    left_side = np.vstack((top_left, bottom_left))
    right_side = np.vstack((top_right, bottom_right))
    x = np.hstack((left_side, right_side))
    return x

def solve_08ed6ac7(x):
    color_numbers = [1,2,3,4]

    len_dict = {}

    for idx in range(len(x)):
        len_dict[idx] = np.count_nonzero(x[:, idx])

    for color_number in color_numbers:
        max_idx = max(len_dict, key=len_dict.get)
        max_col = x[:, max_idx]
        max_col[np.nonzero(max_col)] = color_number
        x[:, max_idx] = max_col
        len_dict.pop(max_idx)

    return x

def solve_d687bc17(x):
    left = list(x[:,0])
    right = list(x[:,-1])
    top = list(x[0,:])
    bottom = list(x[-1,:])

    left_color = max(left, key=left.count)
    rows, cols = np.where(x[:,1:]==left_color)
    for i in range(len(rows)):
        x[rows[i], 1] = left_color
        x[rows[i], cols[i]+1] = 0

    right_color = max(right, key=right.count)
    rows, cols = np.where(x[:,:-2]==right_color)
    for i in range(len(rows)):
        x[rows[i], -2] = right_color
        x[rows[i], cols[i]] = 0

    top_color = max(top, key=top.count)
    rows, cols = np.where(x[1:,:]==top_color)
    for i in range(len(rows)):
        x[1, cols[i]] = top_color
        x[rows[i]+1, cols[i]] = 0

    bottom_color = max(bottom, key=bottom.count)
    rows, cols = np.where(x[:-2,:]==bottom_color)
    for i in range(len(rows)):
        x[-2, cols[i]] = bottom_color
        x[rows[i], cols[i]] = 0

    all_colors = list(np.unique(x))

    for used_colors in [0, left_color, right_color, top_color, bottom_color]:
        all_colors.remove(used_colors)

    for unused_colors in all_colors:
        rows, cols = np.where(x==unused_colors)
        for i in range(len(rows)):
            x[rows[i], cols[i]] = 0

    return x

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

