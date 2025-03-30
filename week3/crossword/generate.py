import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            # Create a copy to avoid modifying set during iteration
            words_to_remove = set()
            for word in self.domains[var]:
                if len(word) != var.length:
                    words_to_remove.add(word)

            # Remove words of incorrect length
            for word in words_to_remove:
                self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]

        # if there's no overlap, no revision needed
        if overlap is None:
            return False

        x_idx, y_idx = overlap

        # check each word in x's domain
        words_to_remove = set()
        for x_word in self.domains[x]:
            # check if there's at least one compatible word in y's domain
            if not any(x_word[x_idx] == y_word[y_idx] for y_word in self.domains[y]):
                words_to_remove.add(x_word)
                revised = True

        # remove incompatible words from x's domain
        for word in words_to_remove:
            self.domains[x].remove(word)

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # initialize queue of arcs to process
        if arcs is None:
            queue = [(x, y) for x in self.crossword.variables
                     for y in self.crossword.neighbors(x)]
        else:
            queue = arcs.copy()

        # process arcs until queue is empty
        while queue:
            x, y = queue.pop(0)

            if self.revise(x, y):
                # if x's domain is empty, problem is unsolvable
                if not self.domains[x]:
                    return False

                # add arcs for neighbors of x (except y) back to queue
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(var in assignment for var in self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check that all values are distinct
        if len(set(assignment.values())) != len(assignment):
            return False

        # check that all words have correct length
        for var, word in assignment.items():
            if len(word) != var.length:
                return False

        # check that there are no conflicts between neighbors
        for var1 in assignment:
            for var2 in self.crossword.neighbors(var1):
                if var2 in assignment:
                    # get the overlap indices
                    overlap = self.crossword.overlaps[var1, var2]
                    i, j = overlap

                    # check if characters at overlap match
                    if assignment[var1][i] != assignment[var2][j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # dictionary to store number of ruled-out values for each word
        ruled_out = {}

        # get unassigned neighbors
        unassigned_neighbors = [n for n in self.crossword.neighbors(var)
                                if n not in assignment]

        # for each word in var's domain
        for word in self.domains[var]:
            ruled_out[word] = 0

            for neighbor in unassigned_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                i, j = overlap

                # count how many values this would rule out
                for neighbor_word in self.domains[neighbor]:
                    if word[i] != neighbor_word[j]:
                        ruled_out[word] += 1

        # return sorted domain values
        return sorted(self.domains[var], key=lambda x: ruled_out[x])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get all unassigned variables
        unassigned = [v for v in self.crossword.variables if v not in assignment]

        # return None if no unassigned variables
        if not unassigned:
            return None

        # sort by minimum remaining values, then by degree (most neighbors)
        return min(unassigned,
                   key=lambda v: (len(self.domains[v]),
                                  -len(self.crossword.neighbors(v))))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # try assigning values to the variable
        for value in self.order_domain_values(var, assignment):
            # create a new assignment with the new value
            new_assignment = assignment.copy()
            new_assignment[var] = value

            # check if assignment is consistent
            if self.consistent(new_assignment):
                # recursive call with new assignment
                result = self.backtrack(new_assignment)

                # if successful, return the result
                if result is not None:
                    return result

        # if no value works, return None (backtrack)
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
