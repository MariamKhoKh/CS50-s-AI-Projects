# Knights and Knaves Puzzle Solver

## Overview
This project implements solutions for the classic "Knights and Knaves" logic puzzles created by Raymond Smullyan. The puzzles involve characters who are either knights (always tell the truth) or knaves (always lie). Using propositional logic, we can determine which character is which based on their statements.

## Files
- `logic.py`: Contains the implementation of logical symbols and operations.
- `puzzle.py`: Contains the knowledge bases for each puzzle and the main program that solves them.

## Puzzle Rules
In these puzzles:
- Each character is either a knight or a knave (not both).
- Knights always tell the truth.
- Knaves always lie.

## Solutions Explained

### Puzzle 0: The Single Character
**Puzzle:** Character A says "I am both a knight and a knave."

**Solution:**
```python
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Biconditional(AKnight, And(AKnight, AKnave))
)
```

**Explanation:**
1. `Or(AKnight, AKnave)`: A is either a knight or a knave.
2. `Not(And(AKnight, AKnave))`: A cannot be both a knight and a knave.
3. `Biconditional(AKnight, And(AKnight, AKnave))`: If A is a knight, then A's statement must be true. If A is a knave, then A's statement must be false.

A's statement is "I am both a knight and a knave." This is impossible because of rule 2. Thus:
- If A were a knight, A's statement would have to be true, which is impossible.
- If A were a knave, A's statement would have to be false, which is possible.

Therefore, A must be a knave.

### Puzzle 1: Knaves Accusation
**Puzzle:** Character A says "We are both knaves." Character B says nothing.

**Solution:**
```python
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Biconditional(AKnight, And(AKnave, BKnave))
)
```

**Explanation:**
1. First four lines: A and B are each either a knight or a knave (not both).
2. `Biconditional(AKnight, And(AKnave, BKnave))`: If A is a knight, then A's statement "We are both knaves" must be true. If A is a knave, then A's statement must be false.

Let's analyze A's statement:
- If A were a knight, A would be saying "We are both knaves," which would include A being a knave. This is a contradiction.
- If A were a knave, A's statement would be false, meaning it's not the case that both A and B are knaves. This allows for two possibilities:
  * A is a knave and B is a knight
  * Both A and B are knights (which contradicts A being a knave)

Therefore, A must be a knave and B must be a knight.

### Puzzle 2: Same or Different
**Puzzle:** Character A says "We are the same kind." Character B says "We are of different kinds."

**Solution:**
```python
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)
```

**Explanation:**
1. First four lines: A and B are each either a knight or a knave (not both).
2. `Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave)))`: If A is a knight, then A's statement "We are the same kind" must be true. This means either both are knights or both are knaves.
3. `Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))`: If B is a knight, then B's statement "We are of different kinds" must be true. This means one is a knight and one is a knave.

Let's analyze the possible combinations:
- If A is a knight and B is a knight:
  * A's statement is true (they are the same kind)
  * B's statement is false (they are not of different kinds)
  * This is a contradiction because knights always tell the truth.

- If A is a knight and B is a knave:
  * A's statement is false (they are not the same kind)
  * B's statement is false (they are not of different kinds)
  * This is a contradiction because knights always tell the truth.

- If A is a knave and B is a knight:
  * A's statement is false (they are not the same kind)
  * B's statement is true (they are of different kinds)
  * This is consistent!

- If A is a knave and B is a knave:
  * A's statement is true (they are the same kind)
  * B's statement is true (they are of different kinds)
  * This is a contradiction because knaves always lie.

Therefore, A must be a knave and B must be a knight.

### Puzzle 3: Complex Statements
**Puzzle:** 
- A says either "I am a knight." or "I am a knave." (we don't know which)
- B says "A said 'I am a knave.'"
- B says "C is a knave."
- C says "A is a knight."

**Solution:**
```python
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight)
)
```

**Explanation:**
1. First six lines: A, B, and C are each either a knight or a knave (not both).
2. `Biconditional(BKnight, Biconditional(AKnight, AKnave))`: If B is a knight, then B's statement "A said 'I am a knave'" must be true. This claim is actually impossible because:
   - If A were a knight saying "I am a knave", A would be lying, which knights cannot do.
   - If A were a knave saying "I am a knave", A would be telling the truth, which knaves cannot do.
   - Therefore, A could not have said "I am a knave".
   - So B's statement is false, meaning B must be a knave.
3. `Biconditional(BKnight, CKnave)`: If B is a knight, then B's statement "C is a knave" must be true. Since we know B is a knave, this statement must be false, so C must be a knight.
4. `Biconditional(CKnight, AKnight)`: If C is a knight, then C's statement "A is a knight" must be true. Since we know C is a knight, this means A must be a knight.

Therefore, A is a knight, B is a knave, and C is a knight.

## Running the Code
To run the code, simply execute:
```
python puzzle.py
```

The output will tell you which character is a knight and which is a knave for each puzzle.

## Key Concepts

### Propositional Logic
- **Symbols**: Represent basic propositions (e.g., "A is a knight")
- **Operators**:
  - `And`: Conjunction (both statements must be true)
  - `Or`: Disjunction (at least one statement must be true)
  - `Not`: Negation (the statement must be false)
  - `Implication`: If-then statement
  - `Biconditional`: If and only if statement

### Model Checking
The code uses a model checking algorithm to determine if a given knowledge base entails a particular query. It systematically checks all possible truth assignments to the symbols to see if the query must be true whenever the knowledge base is true.
