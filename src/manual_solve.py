#!/usr/bin/python

### Name: Jamie Keating
### Student Number: 20235761
### Date: 14th December 2020
### GitHub Repo: https://github.com/jamiekeating/ARC

import os, sys
import json
import numpy as np
import re

### Code to manually solve three problems from the ARC challenge.

def solve_7fe24cdd(x):
    # The output grid is composed of four copies of the input grid. Based on
    # the examples given, the input is always a square grid with dimensions
    # n x n and the output is always a square grid with dimensions 2n x 2n. The
    # top left quadrant of the output grid is the input grid. The top right
    # quadrant is the input grid rotated by 90 degrees clockwise. The bottom
    # right quadrant is the input grid rotated by 180 degrees clockwise. And
    # the bottom left quadrant is the input grid rotated by 90 degrees anti-clockwise.
    # All training/test grids solved correctly.
    
    # Top left quadrant is the input grid (x).
    top_left = x
    # Rotate top left grid by 90 degrees anti-clockwise by reversing the order of
    # the list elements to get the bottom left quadrant.
    bottom_left = np.array(list(reversed(list(zip(*top_left)))))
    # Rotate bottom left grid by 90 degrees anti-clockwise by reversing the order
    # of the list elements to get the bottom right quadrant.
    bottom_right = np.array(list(reversed(list(zip(*bottom_left)))))
    # Rotate bottom right grid by 90 degrees anti-clockwise by reversing the order
    # of the list elements to get the top right quadrant.
    top_right = np.array(list(reversed(list(zip(*bottom_right)))))
    # Vertically stack top left and bottom left quadrants to create the left side
    # of the output grid.
    left_side = np.vstack((top_left, bottom_left))
    # Vertically stack top right and bottom right quadrants to create the right
    # side of the output grid.
    right_side = np.vstack((top_right, bottom_right))
    # Horizontally stack the left and right sides to create the final output grid. 
    x = np.hstack((left_side, right_side))

    # Return output grid.
    return x

def solve_08ed6ac7(x):
    # The output grid is the same layout as the input grid, except the grey squares in
    # each column of the output grid are re-coloured based on the number of grey squares
    # in the column. For the column with the most grey squares, the grey squares are
    # coloured blue. For the column with the second most grey squares, the grey squares
    # are coloured red. For the column with the third most grey squares, the grey squares
    # are coloured green. For the column with the fewest grey squares, the grey squares
    # are coloured yellow. Based on the examples, the position and order of the columns
    # may vary but the output colours are always blue, red, green, and yellow.
    # All training/test grids solved correctly.
    
    # Define a reference list of output colours based on the colour IDs.
    colour_numbers = [1,2,3,4]

    # Create an empty dictionary to store the number of non-zero (grey) elements for each
    # column of the input grid.
    len_dict = {}

    # For each column in the grid, count the number of non-zero elements and store the
    # value in len_dict where the column index is the key.
    for idx in range(len(x)):
        len_dict[idx] = np.count_nonzero(x[:, idx])

    # Assign colours to each column containing non-zero elements. The colours in colour_numbers
    # list are ordered. For each colour ID in colour_numbers, perform the following loop: 
    for colour_number in colour_numbers:
        # Get the dictionary value (column index) with the highest number of non-zero elements.
        max_idx = max(len_dict, key=len_dict.get)
        # Get the column from input grid corresponding to the column index above.
        max_col = x[:, max_idx]
        # Change the non-zero values in the column to the correspoonding colour number.
        max_col[np.nonzero(max_col)] = colour_number
        # Update the column in the input grid with the new values.
        x[:, max_idx] = max_col
        # Remove the column index from len_dict so that in the next loop, the max value
        # will be different.
        len_dict.pop(max_idx)

    # Return output grid.
    return x

def solve_d687bc17(x):
    # The example inputs show m x n grids where the border square for each edge is a
    # different colour. There are also coloured cells scattered across the grid, within
    # the coloured border. The solution for the challenge is to re-position the scattered
    # squares where its colour matches one of th the edges. Scattered squares that do not
    # have a corresponding edge are deleted (coloured black). Where a scattered square is
    # re-positioned, it is moved to be adjacent to the matching coloured edge. Where the
    # coloured edge is on the right or left side, the scattered square maintains the same
    # row index, only the column index is changed. Where the coloured edge is on the top
    # or bottom, the scattered square maintains the same column index, only the row index
    # is changed. Based on the examples, the colours of each edge may vary.
    # All training/test grids solved correctly.

    # Extract the values of the left and right columns and the top and bottom rows of the
    # grid. These will be used to determine the colours of each edge.
    left = list(x[:,0])
    right = list(x[:,-1])
    top = list(x[0,:])
    bottom = list(x[-1,:])

    # For the left side, count the colour IDs. The colour ID with the highest frequency count
    # is the deemed to be the colour of the left edge.
    left_colour = max(left, key=left.count)
    # For the rest of the grid (excluding the left edge) search for scattered squares where the
    # colour matches the left edge.
    rows, cols = np.where(x[:,1:]==left_colour)
    # For each scattered square matching the colour of the left edge, change the colour of
    # the square adjacent to the left edge on the same row to the same colour. Then change
    # the colour of the scattered square to black.
    for i in range(len(rows)):
        x[rows[i], 1] = left_colour
        x[rows[i], cols[i]+1] = 0

    # Repeat the process for the left side for the right, top and bottom edges.
    right_colour = max(right, key=right.count)
    rows, cols = np.where(x[:,:-2]==right_colour)
    for i in range(len(rows)):
        x[rows[i], -2] = right_colour
        x[rows[i], cols[i]] = 0

    top_colour = max(top, key=top.count)
    rows, cols = np.where(x[1:,:]==top_colour)
    for i in range(len(rows)):
        x[1, cols[i]] = top_colour
        x[rows[i]+1, cols[i]] = 0

    bottom_colour = max(bottom, key=bottom.count)
    rows, cols = np.where(x[:-2,:]==bottom_colour)
    for i in range(len(rows)):
        x[-2, cols[i]] = bottom_colour
        x[rows[i], cols[i]] = 0

    # The last step is to remove the scattered squares that do not have matching edges. To do
    # that, create a list of all colours in the input grid and remove the colours used for the
    # edges.
    all_colours = list(np.unique(x))

    for used_colours in [0, left_colour, right_colour, top_colour, bottom_colour]:
        all_colours.remove(used_colours)

    # Scattered squares matching the remaining (unused) colours are changed to black.
    for unused_colours in all_colours:
        rows, cols = np.where(x==unused_colours)
        for i in range(len(rows)):
            x[rows[i], cols[i]] = 0

    # Return output grid.
    return x

### Reflection:
#
# In Chollet's paper, The Measure of Intelligence (https://arxiv.org/abs/1911.01547), he outlines
# the important differences between benchmarking artificial intelligence for specific tasks and
# benchmarking for general artificial intelligence. In short, the measure of general intelligence
# should be the ability to learn skills rather than the performance of the skill itself. Solutions
# to the tasks in the ARC dataset are so varied that a single narrowly-defined algorithm could not
# solve all of them, even if it was highly skilled in solving one specific problem type. For some
# tasks in the ARC dataset, it is difficult to even articulate in a concise manner the exact steps
# required to solve the task, even if the answer appears obvious.
#
# To solve these tasks with hand-coded solutions, I used basic python and some useful functions from
# Numpy. For the tasks I chose I did not need to use any other libraries. Each of the solutions take
# advantage of the matrix structure of the input/output grids and the ability to slice matrices into
# rows and columns using Numpy. In all cases it was important to identify the location and orientation
# of shapes in the input and output grids. However, this similarity did not simplify the implementation
# because the exact requirement to recognise shapes and their location was slightly different in each
# case. While there were some similarities across the solutions, the differences were more apparent.
# For some tasks it was important to keep track of the size of the shapes in the grid and in others
# the count of shapes was important. For some tasks the shapes were not important but the repeated
# patterns were. And in others the relative position of shapes was important. In all cases it was
# important to understand the entire "situation" to solve the task. Knowing the value of each square
# in the input and output grids in the test datasets is meaningless without understanding the
# relationship between all squares. Chollet refers to this as the "situation space". This is reminiscent
# of the feature hierarchy in deep learning.
#
# The tasks in the ARC dataset highlight the layers and nuance of intelligence required to solve even
# apparently simple tasks. The individual transformations required to solve simple tasks are trivial
# for a human, but the intelligent orchestration of such tasks is beyond the current state of the art -
# from Chollet's paper "ARC does not appear to be approachable by any existing machine learning
# technique (including Deep Learning), due to its focus on broad generalization and few-shot learning".
# Chollet expects that a solution to the ARC dataset will take the form of a program synthesis engine
# which will use a domain-specific language capable of expressing all possible solution programs for
# any ARC task and generate candidate programs and solutions from each. The successful development of
# a human-level solver would represent the ability to program an AI based on demonstration alone and
# to do tasks which require human-like intelligence. In the meantime, the ARC dataset and challenge
# represent a useful testing ground for new approaches to AI.

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

