# WordPiece Tokenization

## 📌 Project Overview

This project demonstrates **WordPiece Tokenization**, a subword tokenization technique widely used in Natural Language Processing (NLP) models such as **BERT**.

WordPiece breaks words into smaller subword units. This helps NLP models handle unknown words, rare words, and different word forms more effectively.

## 🎯 Objectives

* Understand the concept of WordPiece Tokenization
* Learn how words are divided into subword tokens
* Handle unknown and rare words efficiently
* Understand the role of subword tokenization in NLP
* Implement WordPiece Tokenization using Python

## 🔍 How WordPiece Tokenization Works

WordPiece starts with smaller units and combines them based on their frequency and usefulness in the training data.

For example:

```text
Playing → play + ##ing
Unwanted → un + ##wanted
```

The `##` symbol indicates that the token is a continuation of the previous token.

## 🧠 Example

Input:

```text
"I am playing football"
```

Possible WordPiece tokens:

```text
["I", "am", "play", "##ing", "football"]
```

The tokens can then be converted into numerical **Token IDs**, which are given as input to an NLP model.

## 🛠️ Technologies Used

* Python
* NLP
* Hugging Face Transformers
* BERT Tokenizer

## 📦 Installation

Install the required library:

```bash
pip install transformers
```

## 💻 Implementation

```python
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

text = "I am playing football"

tokens = tokenizer.tokenize(text)

print("Tokens:", tokens)

token_ids = tokenizer.convert_tokens_to_ids(tokens)

print("Token IDs:", token_ids)
```

## 📊 Output

Example output:

```text
Tokens: ['i', 'am', 'playing', 'football']

Token IDs: [1045, 2572, 2652, 2374]
```

The exact output depends on the tokenizer and vocabulary being used.

## ⭐ Advantages

* Handles rare and unknown words better than word-level tokenization
* Reduces the problem of out-of-vocabulary words
* Can represent new words using smaller subword units
* Useful for multilingual and large-sca
