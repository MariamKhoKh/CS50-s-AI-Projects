import nltk
import sys
import re

# Download necessary NLTK data packages
nltk.download('punkt')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det Adj N | NP PP | Det Adj Adj N | Det Adj Adj Adj N
VP -> V | V NP | V PP | V NP PP | Adv V | V Adv
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Simple approach without using nltk.word_tokenize
    # Split by whitespace and punctuation
    words_raw = re.findall(r'\b\w+\b', sentence.lower())

    # Filter out words without alphabetic characters
    result = [word for word in words_raw if any(c.isalpha() for c in word)]

    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    # Function to check if the tree contains any NP subtrees
    def has_np_subtree(t):
        if not isinstance(t, nltk.Tree):
            return False

        for child in t:
            if isinstance(child, nltk.Tree) and child.label() == "NP":
                return True
            if has_np_subtree(child):
                return True
        return False

    # Function to find all NP chunks
    def find_chunks(t):
        if isinstance(t, nltk.Tree):
            # If this is an NP and it doesn't contain other NPs
            if t.label() == "NP":
                contains_np = False
                for child in t:
                    if isinstance(child, nltk.Tree) and child.label() == "NP":
                        contains_np = True
                        break

                if not contains_np:
                    chunks.append(t)

            # Continue searching in all children
            for child in t:
                find_chunks(child)

    find_chunks(tree)
    return chunks


if __name__ == "__main__":
    main()