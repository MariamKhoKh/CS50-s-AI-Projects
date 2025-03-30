# Crossword Puzzle Generator

This project implements a constraint satisfaction problem (CSP) solver to automatically generate crossword puzzles. 
Given a crossword structure and a list of words, the program finds a valid assignment of words to the crossword grid 
that satisfies all constraints.

## Overview

A crossword puzzle consists of a grid of white and black squares. The white squares must be filled with letters to form words that read across and down. 
The program takes two inputs:
- A structure file defining the grid layout
- A words file containing possible words to use in the puzzle

## Files

- `crossword.py`: Defines the `Variable` and `Crossword` classes for representing the puzzle
- `generate.py`: Implements the CSP solver using backtracking search with constraint propagation

## How It Works

The program solves the crossword puzzle by modeling it as a constraint satisfaction problem:

1. **Variables**: Each sequence of white squares in the grid (across or down)
2. **Domains**: Each variable can be assigned any word from the vocabulary that has the correct length
3. **Constraints**:
   - **Unary constraints**: Words must have the correct length
   - **Binary constraints**: Overlapping variables must share the same letter at intersections
   - **Additional constraint**: All assigned words must be different


## Heuristics

To improve efficiency, the program implements several heuristics:

1. **Minimum Remaining Values (MRV)**: Select the variable with the fewest legal values in its domain first
2. **Degree Heuristic**: If there's a tie in MRV, choose the variable with the most constraints on other variables
3. **Least-Constraining Value**: Order domain values by how many options they eliminate for neighboring variables

## Usage

Run the program with the following command:

```
python generate.py structure_file words_file [output_image]
```
