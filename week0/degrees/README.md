# Degrees of Separation
This program finds the shortest path between any two actors by determining the "degrees of separation" between them. Two actors are connected if they starred in the same movie. The program uses breadth-first search to find the shortest path from one actor to another through shared movie appearances.
Original problem statement: [Degrees](https://cs50.harvard.edu/ai/2024/projects/0/degrees/)

## Solution Overview
The core of the solution is the shortest_path function which implements a breadth-first search algorithm to find the shortest connection between two actors:

We begin with a source actor and search for a path to the target actor. A queue is used to explore actors in order of their distance from the source. For each actor, we check all their neighbors, meaning other actors they have worked with. To prevent cycles, we keep track of visited actors. If the target actor is found, we reconstruct the path by following parent references. If no path exists, the function returns None.

The solution uses the provided utility classes (Node, QueueFrontier) to manage the search process.

## How to Use

Run the program with a dataset:
```bash 
python degrees.py [dataset]
```
Where [dataset] is either small or large

Enter the names of two actors when prompted
The program will output:

The number of degrees of separation
The specific movies that connect the actors


## Example
```bash python degrees.py small
Loading data...
Data loaded.
Name: Kevin Bacon
Name: Tom Hanks
1 degrees of separation.
1: Kevin Bacon and Tom Hanks starred in Apollo 13
```