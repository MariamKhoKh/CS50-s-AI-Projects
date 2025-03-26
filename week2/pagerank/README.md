# PageRank

This project implements the **PageRank algorithm**, which calculates the importance of web pages based on their links. It uses two approaches:
1. **Sampling-based PageRank**
2. **Iterative PageRank** 

## How It Works
The PageRank algorithm assigns a probability score to each page, indicating how likely a user is to land on that page by clicking links randomly.

### Key Concepts
- **Damping Factor (0.85 by default)**: Represents the probability that a user follows a link instead of jumping to a random page.
- **Transition Model**: Defines the probability of moving from one page to another.
- **Sampling Method**: Simulates a user navigating the pages randomly.
- **Iterative Convergence**: Repeatedly updates PageRank values until they stabilize.

## How to Run the Code
1. Open a terminal and navigate to the project folder.
2. Run the following command:
   ```sh
   python pagerank.py corpusX (X = 0, 1 0r 2)
   ```

## Understanding the Results
When you run the script, it outputs PageRank values for each page using both methods:
- **Sampling Method**: Slightly different values each run due to randomness.
- **Iterative Method**: Consistent values every time, as it solves equations mathematically.

Example output:
```
PageRank Results from Sampling (n = 10000)
  1.html: 0.2155
  2.html: 0.4301
  3.html: 0.2235
  4.html: 0.1309

PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
```

## Summary
- The project calculates PageRank using both **random sampling** and **iterative convergence**.
- The **iterative approach is deterministic**, while **sampling has slight variations**.
- Running `pagerank.py corpus_folder` computes and prints PageRank values.


