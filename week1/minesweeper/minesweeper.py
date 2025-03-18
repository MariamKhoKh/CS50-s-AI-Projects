import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of cells equals the count, all cells must be mines
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If count is 0, all cells must be safe
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell is not in the sentence, nothing to do
        if cell not in self.cells:
            return

        # Remove the cell from the sentence
        self.cells.remove(cell)
        # Decrease the count since we've removed a mine
        self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell is not in the sentence, nothing to do
        if cell not in self.cells:
            return

        # Remove the cell from the sentence (count stays the same since it wasn't a mine)
        self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark cell as a move that has been made
        self.moves_made.add(cell)

        # Mark cell as safe
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base
        # Get all neighboring cells
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Skip the cell itself
                if (i, j) == cell:
                    continue
                # Make sure we're within the board bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # Remove cells that are already known to be safe or mines
        unknown_neighbors = set()
        mine_count = count

        for neighbor in neighbors:
            if neighbor in self.safes:
                # If it's safe, don't include it in the sentence
                continue
            elif neighbor in self.mines:
                # If it's a mine, don't include it but decrement the count
                mine_count -= 1
                continue
            unknown_neighbors.add(neighbor)

        # Create a new sentence with unknown neighbors
        if unknown_neighbors:
            new_sentence = Sentence(unknown_neighbors, mine_count)
            # Only add if it's not already in the knowledge base
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        # Check for new mines and safe cells in all sentences
        self.check_knowledge()

        # Check for subset relationships to infer new knowledge
        self.infer_from_subsets()

        # Keep checking knowledge until no new inferences can be made
        self.repeatedly_check_knowledge()

    def check_knowledge(self):
        """Helper function to check for new mines and safe cells in all sentences"""
        for sentence in self.knowledge:
            # Check for known mines and mark them
            mines = sentence.known_mines()
            for mine in mines:
                self.mark_mine(mine)

            # Check for known safe cells and mark them
            safes = sentence.known_safes()
            for safe in safes:
                self.mark_safe(safe)

    def infer_from_subsets(self):
        """Helper function to check for subset relationships between sentences"""
        # Make a copy of knowledge to avoid modifying while iterating
        knowledge_copy = self.knowledge.copy()

        # Check each pair of sentences for subset relationships
        for s1 in knowledge_copy:
            for s2 in knowledge_copy:
                # Skip if they're the same sentence or either has no cells
                if s1 == s2 or len(s1.cells) == 0 or len(s2.cells) == 0:
                    continue

                # If s1 is a subset of s2
                if s1.cells.issubset(s2.cells):
                    # Create a new sentence with the difference and count difference
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count

                    # Create a new sentence and add to knowledge if not already present
                    if new_cells and new_count >= 0:
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)

    def repeatedly_check_knowledge(self):
        """
        Repeatedly checks knowledge base until no new inferences can be made
        """
        # Keep track of previous knowledge state
        previous_mines = len(self.mines)
        previous_safes = len(self.safes)

        # Keep checking until no new cells are marked
        while True:
            # Check for new mines and safes
            self.check_knowledge()

            # Check for subset relationships
            self.infer_from_subsets()

            # Clean up empty sentences
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

            # If no new mines or safes were found, we're done
            if len(self.mines) == previous_mines and len(self.safes) == previous_safes:
                break

            # Update counts
            previous_mines = len(self.mines)
            previous_safes = len(self.safes)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Find safe cells that haven't been moved on yet
        safe_moves = self.safes - self.moves_made

        # Return a random safe move if available
        if safe_moves:
            return random.choice(list(safe_moves))

        # No safe moves available
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Get all possible moves (all board positions)
        all_possible_moves = set((i, j) for i in range(self.height) for j in range(self.width))

        # Remove mines and moves already made
        available_moves = all_possible_moves - self.mines - self.moves_made

        # Return a random move if available
        if available_moves:
            return random.choice(list(available_moves))

        # No moves available
        return None