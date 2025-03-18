from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both
    Not(And(AKnight, AKnave)),
    # If A is a knight, what A says is true; if A is a knave, what A says is false
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both
    Not(And(AKnight, AKnave)),
    # B is either a knight or a knave
    Or(BKnight, BKnave),
    # B cannot be both
    Not(And(BKnight, BKnave)),
    # If A is a knight, what A says is true; if A is a knave, what A says is false
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both
    Not(And(AKnight, AKnave)),
    # B is either a knight or a knave
    Or(BKnight, BKnave),
    # B cannot be both
    Not(And(BKnight, BKnave)),
    # If A is a knight, what A says is true; if A is a knave, what A says is false
    # "Same kind" means both knights or both knaves
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If B is a knight, what B says is true; if B is a knave, what B says is false
    # "Different kinds" means one knight and one knave
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    # A cannot be both
    Not(And(AKnight, AKnave)),
    # B is either a knight or a knave
    Or(BKnight, BKnave),
    # B cannot be both
    Not(And(BKnight, BKnave)),
    # C is either a knight or a knave
    Or(CKnight, CKnave),
    # C cannot be both
    Not(And(CKnight, CKnave)),

    # B's first claim: A said "I am a knave"
    # If A said "I am a knave", then:
    #   - If A is a knight, then "I am a knave" would be true (contradiction)
    #   - If A is a knave, then "I am a knave" would be false (also contradiction)
    # So if A claimed "I am a knave", this would be: Biconditional(AKnight, AKnave)
    # And B's claim is true if B is a knight
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),

    # B's second claim: "C is a knave"
    Biconditional(BKnight, CKnave),

    # C's claim: "A is a knight"
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
