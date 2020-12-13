# The Abstraction and Reasoning Corpus (ARC)

This repository contains the ARC task data, as well as a browser-based interface for humans to try their hand at solving the tasks manually. This repositiory also contains the hand-coded solutions for three tasks, as required for Assignment 3 in the Programming and Tools for Artificial Intelligence module, part of the M.Sc. in Artificial Intelligence at NUI Galway.

*"ARC can be seen as a general artificial intelligence benchmark, as a program synthesis benchmark, or as a psychometric intelligence test. It is targeted at both humans and artificially intelligent systems that aim at emulating a human-like form of general fluid intelligence."*

A complete description of the dataset, its goals, and its underlying logic, can be found in: [The Measure of Intelligence](https://arxiv.org/abs/1911.01547).

As a reminder, a test-taker is said to solve a task when, upon seeing the task for the first time, they are able to produce the correct output grid for *all* test inputs in the task (this includes picking the dimensions of the output grid). For each test input, the test-taker is allowed 3 trials (this holds for all test-takers, either humans or AI).


## Task file format

The `data` directory contains two subdirectories:

- `data/training`: contains the task files for training (400 tasks). Use these to prototype your algorithm or to train your algorithm to acquire ARC-relevant cognitive priors.
- `data/evaluation`: contains the task files for evaluation (400 tasks). Use these to evaluate your final algorithm. To ensure fair evaluation results, do not leak information from the evaluation set into your algorithm (e.g. by looking at the evaluation tasks yourself during development, or by repeatedly modifying an algorithm while using its evaluation score as feedback).

The tasks are stored in JSON format. Each task JSON file contains a dictionary with two fields:

- `"train"`: demonstration input/output pairs. It is a list of "pairs" (typically 3 pairs).
- `"test"`: test input/output pairs. It is a list of "pairs" (typically 1 pair).

A "pair" is a dictionary with two fields:

- `"input"`: the input "grid" for the pair.
- `"output"`: the output "grid" for the pair.

A "grid" is a rectangular matrix (list of lists) of integers between 0 and 9 (inclusive). The smallest possible grid size is 1x1 and the largest is 30x30.

When looking at a task, a test-taker has access to inputs & outputs of the demonstration pairs, plus the input(s) of the test pair(s). The goal is to construct the output grid(s) corresponding to the test input grid(s), using 3 trials for each test input. "Constructing the output grid" involves picking the height and width of the output grid, then filling each cell in the grid with a symbol (integer between 0 and 9, which are visualized as colors). Only *exact* solutions (all cells match the expected answer) can be said to be correct.


## Usage of the testing interface

The testing interface is located at `apps/testing_interface.html`. Open it in a web browser (Chrome recommended). It will prompt you to select a task JSON file.

After loading a task, you will enter the test space, which looks like this:

![test space](https://arc-benchmark.s3.amazonaws.com/figs/arc_test_space.png)

On the left, you will see the input/output pairs demonstrating the nature of the task. In the middle, you will see the current test input grid. On the right, you will see the controls you can use to construct the corresponding output grid.

You have access to the following tools:

### Grid controls

- Resize: input a grid size (e.g. "10x20" or "4x4") and click "Resize". This preserves existing grid content (in the top left corner).
- Copy from input: copy the input grid to the output grid. This is useful for tasks where the output consists of some modification of the input.
- Reset grid: fill the grid with 0s.

### Symbol controls

- Edit: select a color (symbol) from the color picking bar, then click on a cell to set its color.
- Select: click and drag on either the output grid or the input grid to select cells.
    - After selecting cells on the output grid, you can select a color from the color picking to set the color of the selected cells. This is useful to draw solid rectangles or lines.
    - After selecting cells on either the input grid or the output grid, you can press C to copy their content. After copying, you can select a cell on the output grid and press "V" to paste the copied content. You should select the cell in the top left corner of the zone you want to paste into.
- Floodfill: click on a cell from the output grid to color all connected cells to the selected color. "Connected cells" are contiguous cells with the same color.

### Answer validation

When your output grid is ready, click the green "Submit!" button to check your answer. We do not enforce the 3-trials rule.

After you've obtained the correct answer for the current test input grid, you can switch to the next test input grid for the task using the "Next test input" button (if there is any available; most tasks only have one test input).

When you're done with a task, use the "load task" button to open a new task.

### Hand-Coded Solutions

Hand-coded solutions to three tasks (d687bc17, 08ed6ac7 and 7fe24cdd) have been added in src/manual_solve.py.

To reflect on the assignment: In Chollet's paper, [The Measure of Intelligence](https://arxiv.org/abs/1911.01547), he outlines the important differences between benchmarking artificial intelligence for specific tasks and benchmarking for general artificial intelligence. In short, the measure of general intelligence should be the ability to learn skills rather than the performance of the skill itself. Solutions to the tasks in the ARC dataset are so varied that a single narrowly-defined algorithm could not solve all of them, even if it was highly skilled in solving one specific problem type. For some tasks in the ARC dataset, it is difficult to even articulate in a concise manner the exact steps required to solve the task, even if the answer appears obvious.

To solve these tasks with hand-coded solutions, I used basic python and some useful functions from Numpy. For the tasks I chose I did not need to use any other libraries. Each of the solutions take advantage of the matrix structure of the input/output grids and the ability to slice matrices into rows and columns using Numpy. In all cases it was important to identify the location and orientation of shapes in the input and output grids. However, this similarity did not simplify the implementation because the exact requirement to recognise shapes and their location was slightly different in each case. While there were some similarities across the solutions, the differences were more apparent. For some tasks it was important to keep track of the size of the shapes in the grid and in others the count of shapes was important. For some tasks the shapes were not important but the repeated patterns were. And in others the relative position of shapes was important. In all cases it was important to understand the entire "situation" to solve the task. Knowing the value of each square in the input and output grids in the test datasets is meaningless without understanding the relationship between all squares. Chollet refers to this as the "situation space". This is reminiscent of the feature hierarchy in deep learning.

The tasks in the ARC dataset highlight the layers and nuance of intelligence required to solve even apparently simple tasks. The individual transformations required to solve simple tasks are trivial for a human, but the intelligent orchestration of such tasks is beyond the current state of the art - from Chollet's paper "ARC does not appear to be approachable by any existing machine learning technique (including Deep Learning), due to its focus on broad generalization and few-shot learning". Chollet expects that a solution to the ARC dataset will take the form of a program synthesis engine which will use a domain-specific language capable of expressing all possible solution programs for any ARC task and generate candidate programs and solutions from each. The successful development of a human-level solver would represent the ability to program an AI based on demonstration alone and to do tasks which require human-like intelligence. In the meantime, the ARC dataset and challenge represent a useful testing ground for new approaches to AI.