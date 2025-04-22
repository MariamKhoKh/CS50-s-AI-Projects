# BERT Attention Visualization

This project implements a tool to visualize attention patterns in BERT (Bidirectional Encoder Representations from Transformers), a powerful language model. The program predicts masked words in input text and generates visual diagrams of the self-attention mechanisms used by BERT.

## Implementation Details

The solution implements three key functions:

1. `get_mask_token_index`: Locates the position of the [MASK] token in the input sequence.
   - Searches through the token IDs to find the mask token ID
   - Returns the 0-indexed position or None if not found

2. `get_color_for_attention_score`: Converts attention scores to grayscale colors.
   - Takes an attention score between 0 and 1
   - Returns an RGB tuple representing a shade of gray (from black to white)
   - Uses linear scaling: 0 → (0,0,0), 1 → (255,255,255)

3. `visualize_attentions`: Generates attention diagrams for all layers and heads.
   - Loops through each attention layer and head
   - Creates visualizations showing how each token attends to other tokens
   - Uses 1-indexed numbering for diagram filenames

## How to Use

1. Run `python mask.py`
2. Enter text with a [MASK] token where you want the model to predict a word
3. The program will:
   - Display the top 3 predicted words for the masked position
   - Generate attention diagrams for all 12 layers × 12 heads (144 total diagrams)
4. Examine the diagrams to identify patterns in how BERT understands language

