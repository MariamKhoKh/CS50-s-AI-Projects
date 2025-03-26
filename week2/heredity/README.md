# Heredity

This project calculates the probability of individuals inheriting a particular gene and whether they exhibit a related trait.
It uses Bayesian probability and considers inheritance patterns from parents.

## How It Works
1. **Load Data**: The program reads a CSV file containing family information.
2. **Generate Possibilities**: It considers different possible gene inheritance scenarios.
3. **Calculate Joint Probability**: The probability of a specific inheritance scenario occurring is computed using probability rules.
4. **Update Probabilities**: The computed probabilities are stored and accumulated.
5. **Normalize Probabilities**: The values are adjusted so they sum to 1.

## Running the Program
Run the following command:
```sh
python heredity.py data/familyX.csv  # X = 0, 1 or 2
```

## Understanding the Output
For each person, the program prints the probabilities of having 0, 1, or 2 copies of the gene and the probability of showing the trait.

## Explanation 
- Every person has **two copies of a gene** (one from each parent).
- The program calculates how likely it is that each person has **0, 1, or 2 copies**.
- If a person's parents are unknown, base probabilities are used.
- If parents are known, inheritance rules determine probabilities.
- The program also checks if having the gene affects the likelihood of showing the trait.
- All possibilities are considered, and final probabilities are displayed.

## Notes
- The program follows **Mendelian genetics** with a small mutation chance.
- It works on different datasets following the same structure.


