# Minesweeper AI Project

## Overview
This project implements an AI that can play Minesweeper using logical inference. The AI uses knowledge representation techniques to keep track of safe moves and mines, and makes decisions based on the information it gathers during gameplay.

## Files
- `minesweeper.py`: Contains the game logic and AI implementation
- `runner.py`: Handles the graphical interface using Pygame

## How to Run
1. Make sure you have Python and Pygame installed
2. Run the game with: `python runner.py`
3. Click "Play Game" to start
4. Either make moves yourself by clicking on cells, or use the "AI Move" button to let the AI play

## How the AI Works

### Knowledge Representation
The AI represents its knowledge about the game using "sentences". Each sentence consists of:
- A set of cells
- A count of how many mines are within that set of cells

For example, if we click on a cell and see the number 3, we know that 3 of the 8 surrounding cells contain mines. This forms a sentence: "3 of these 8 cells are mines".

### The Sentence Class
This class encapsulates logical statements about the game. It provides methods to:

- `known_mines()`: Returns cells that are definitely mines
  - If a sentence has N cells and a count of N, all cells must be mines
  
- `known_safes()`: Returns cells that are definitely safe
  - If a sentence has a count of 0, all cells must be safe
  
- `mark_mine(cell)`: Updates the sentence when a cell is confirmed to be a mine
  - Removes the cell from the set and decreases the count
  
- `mark_safe(cell)`: Updates the sentence when a cell is confirmed to be safe
  - Removes the cell from the set without changing the count

### The MinesweeperAI Class
This class handles the AI's gameplay logic:

- **Knowledge tracking**:
  - `moves_made`: Set of cells that have been clicked
  - `mines`: Set of cells known to be mines
  - `safes`: Set of cells known to be safe
  - `knowledge`: List of sentences about the game

- **Making inferences**:
  - When the AI learns about a new safe cell and its neighboring mine count, it:
    1. Marks the cell as a move that has been made
    2. Marks the cell as safe
    3. Creates a new sentence based on the neighbors
    4. Updates knowledge with new inferences
    5. Uses logical deduction to identify more mines and safe cells

- **Subset inference**:
  - If sentence A is a subset of sentence B, we can create a new sentence (B-A) with count (count_B - count_A)
  - Example: If we know "2 of these 5 cells are mines" and "1 of these 3 cells are mines" (where the 3 cells are a subset of the 5), we can deduce that "1 of the remaining 2 cells is a mine"

- **Making moves**:
  - `make_safe_move()`: Returns a random cell known to be safe
  - `make_random_move()`: Returns a random cell that hasn't been clicked and isn't known to be a mine

### Step-by-Step AI Logic

1. **When the AI learns about a cell**:
   ```
   add_knowledge(cell=(2,3), count=2)
   ```
   - This means cell (2,3) has been clicked and has 2 mines in its neighboring cells

2. **Adding to knowledge**:
   - Mark (2,3) as a move made
   - Mark (2,3) as safe
   - Create a new sentence: "{(1,2), (1,3), (1,4), (2,2), (2,4), (3,2), (3,3), (3,4)} = 2"
   - This means "2 of these 8 cells are mines"

3. **Processing knowledge**:
   - For each sentence, check if all cells are mines or all are safe
   - If a cell is identified as a mine or safe, update all sentences
   - Look for subset relationships between sentences to create new sentences
   - Repeat until no new inferences can be made

4. **Making a move**:
   - Choose a cell known to be safe
   - If no safe cell is known, make a random move (avoiding known mines)

## Example Game Flow

1. First move is always random (AI has no knowledge yet)
2. AI clicks (3,3) and gets count=1 (1 neighboring mine)
3. AI adds a sentence about the 8 neighbors of (3,3)
4. As the game progresses, AI gains more knowledge
5. AI uses logical deduction to identify safe cells and mines
6. AI continues until it either wins or makes a wrong move

## Solution Details

### Key Algorithm Components

1. **Cell Marking**:
   ```python
   def mark_mine(self, cell):
       self.mines.add(cell)
       for sentence in self.knowledge:
           sentence.mark_mine(cell)
   ```
   When a cell is identified as a mine, all sentences are updated.

2. **Creating Sentences**:
   ```python
   # Get all neighboring cells of the clicked cell
   neighbors = set()
   for i in range(cell[0] - 1, cell[0] + 2):
       for j in range(cell[1] - 1, cell[1] + 2):
           # Skip the cell itself and check bounds
           if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
               neighbors.add((i, j))
   ```

3. **Subset Inference**:
   ```python
   # If s1 is a subset of s2
   if s1.cells.issubset(s2.cells):
       # Create a new sentence with the difference
       new_cells = s2.cells - s1.cells
       new_count = s2.count - s1.count
       
       # Add to knowledge if valid
       if new_cells and new_count >= 0:
           new_sentence = Sentence(new_cells, new_count)
           if new_sentence not in self.knowledge:
               self.knowledge.append(new_sentence)
   ```

## Conclusion

This Minesweeper AI demonstrates how logical inference can be used to make decisions in a partially observable environment. The AI builds a knowledge base of logical sentences and uses deduction to determine which cells are safe to click and which contain mines.

By repeating this process of gathering information and making inferences, the AI can often solve Minesweeper boards without having to make random guesses, though some situations will still require guessing when there's insufficient information.