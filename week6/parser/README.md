# Natural Language Parser

This project implements a parser for natural language sentences using context-free grammar rules and NLTK. The parser analyzes English sentences to determine their structure and extracts noun phrases.

## Overview

The parser uses context-free grammar (CFG) to break down sentences into their constituent parts (nouns, verbs, adjectives, etc.) and then identifies the sentence structure. It also implements functionality to extract "noun phrase chunks" - noun phrases that don't contain other noun phrases within them.

## Files

- `parser.py`: Main program that contains the grammar rules and parsing functionality
- `sentences/`: Directory containing sample sentences to parse

## Implementation Details

### Grammar Rules

The parser uses two sets of grammar rules:

1. **Terminal Symbols** (predefined in the assignment):
   - Words categorized by their part of speech (nouns, verbs, adjectives, etc.)

2. **Nonterminal Symbols** (implemented as part of the solution):
   ```
   S -> NP VP | S Conj S
   NP -> N | Det N | Det Adj N | NP PP | Det Adj Adj N | Det Adj Adj Adj N
   VP -> V | V NP | V PP | V NP PP | Adv V | V Adv
   PP -> P NP
   ```
   
   These rules define:
   - A sentence (S) as either a noun phrase followed by a verb phrase, or two sentences joined by a conjunction
   - A noun phrase (NP) as a simple noun or more complex combinations with determiners, adjectives, and prepositional phrases
   - A verb phrase (VP) as a verb, optionally followed by noun phrases, prepositional phrases, or modified by adverbs
   - A prepositional phrase (PP) as a preposition followed by a noun phrase

### Key Functions

#### 1. `preprocess(sentence)`

This function prepares a sentence for parsing by:
- Converting the text to lowercase
- Tokenizing the sentence into individual words
- Filtering out tokens that don't contain at least one alphabetic character

The implementation uses regular expressions to identify words and filter them appropriately.

#### 2. `np_chunk(tree)`

This function extracts all "noun phrase chunks" from a parsed sentence tree:
- Traverses the tree recursively
- Identifies subtrees labeled as "NP" (noun phrases)
- Only includes those that don't contain other NP subtrees within them
- Returns a list of all qualifying noun phrase chunks

The implementation uses helper functions to check if a tree contains NP subtrees and to find all valid NP chunks.

## How It Works

1. The program reads a sentence from a file or user input
2. The sentence is preprocessed into a list of lowercase words
3. The NLTK ChartParser attempts to parse the sentence using the defined grammar
4. If successful, it displays the parse tree(s) and the extracted noun phrase chunks

## Example Output

For the input sentence "Holmes sat":

```
        S
   _____|___
  NP        VP
  |         |
  N         V
  |         |
holmes     sat

Noun Phrase Chunks
holmes
```

## Dependencies

- NLTK (Natural Language Toolkit)
- Python 3.x
- Regular expressions module (re)

## Usage

Run the program with:
```
python parser.py
```

You can also specify a file containing a sentence:
```
python parser.py sentences/1.txt
```