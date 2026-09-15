
from collections import Counter, defaultdict


# ============================================================
# STEP 1: READ RAW DATA
# ============================================================

with open("dataset/rawdata.txt", "r") as file:
    words = [line.strip().lower() for line in file if line.strip()]

word_freq = Counter(words)

print("========== WORD FREQUENCIES ==========")

for word, freq in word_freq.items():
    print(word, ":", freq)


# ============================================================
# STEP 2: INITIAL WORDPIECE SPLIT
# ============================================================

splits = {}

for word in word_freq:
    tokens = []

    for i, char in enumerate(word):
        if i == 0:
            tokens.append(char)
        else:
            tokens.append("##" + char)

    splits[word] = tokens


print("\n========== INITIAL SPLITS ==========")

for word, tokens in splits.items():
    print(word, "->", tokens)


# ============================================================
# STEP 3: INITIAL VOCABULARY
# ============================================================

vocab = set()

for tokens in splits.values():
    vocab.update(tokens)

print("\n========== INITIAL VOCABULARY ==========")

for token in sorted(vocab):
    print(token)


# ============================================================
# STEP 4: TOKEN FREQUENCIES
# ============================================================

def get_token_frequencies(splits, word_freq):

    token_freq = Counter()

    for word, tokens in splits.items():
        frequency = word_freq[word]

        for token in tokens:
            token_freq[token] += frequency

    return token_freq


token_freq = get_token_frequencies(splits, word_freq)

print("\n========== TOKEN FREQUENCIES ==========")

for token, freq in token_freq.items():
    print(token, ":", freq)


# ============================================================
# STEP 5: PAIR FREQUENCIES
# ============================================================

def get_pair_counts(splits, word_freq):

    pair_freq = Counter()

    for word, tokens in splits.items():

        frequency = word_freq[word]

        for i in range(len(tokens) - 1):

            pair = (tokens[i], tokens[i + 1])

            pair_freq[pair] += frequency

    return pair_freq


pair_freq = get_pair_counts(splits, word_freq)

print("\n========== PAIR FREQUENCIES ==========")

for pair, freq in pair_freq.items():
    print(pair, ":", freq)


# ============================================================
# STEP 6: WORDPIECE SCORE
# ============================================================

def calculate_scores(pair_freq, token_freq):

    scores = {}

    for pair, freq in pair_freq.items():

        first_token = pair[0]
        second_token = pair[1]

        score = freq / (
            token_freq[first_token] * token_freq[second_token]
        )

        scores[pair] = score

    return scores


scores = calculate_scores(pair_freq, token_freq)

print("\n========== WORDPIECE SCORES ==========")

for pair, score in scores.items():
    print(pair, ":", round(score, 6))


# ============================================================
# STEP 7: MERGE BEST PAIR
# ============================================================

def merge_pair(splits, pair):

    new_token = pair[0] + pair[1].replace("##", "")

    for word in splits:

        tokens = splits[word]

        new_tokens = []

        i = 0

        while i < len(tokens):

            if i < len(tokens) - 1:

                current_pair = (
                    tokens[i],
                    tokens[i + 1]
                )

                if current_pair == pair:

                    new_tokens.append(new_token)

                    i += 2

                    continue

            new_tokens.append(tokens[i])

            i += 1

        splits[word] = new_tokens

    return new_token


# ============================================================
# STEP 8: TRAIN WORDPIECE TOKENIZER
# ============================================================

desired_vocab_size = len(vocab) + 5

merge_rules = []

print("\n========== WORDPIECE TRAINING ==========")

while len(vocab) < desired_vocab_size:

    pair_freq = get_pair_counts(
        splits,
        word_freq
    )

    if not pair_freq:
        break

    token_freq = get_token_frequencies(
        splits,
        word_freq
    )

    scores = calculate_scores(
        pair_freq,
        token_freq
    )

    best_pair = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_pair]

    new_token = merge_pair(
        splits,
        best_pair
    )

    vocab.add(new_token)

    merge_rules.append(
        (best_pair, new_token)
    )

    print("\nMerge", len(merge_rules))

    print("Best Pair :", best_pair)

    print("Pair Frequency :", pair_freq[best_pair])

    print("Score :", round(best_score, 6))

    print("New Token :", new_token)


# ============================================================
# STEP 9: FINAL SPLITS
# ============================================================

print("\n========== FINAL WORD SPLITS ==========")

for word, tokens in splits.items():
    print(word, "->", tokens)


# ============================================================
# STEP 10: FINAL VOCABULARY
# ============================================================

print("\n========== FINAL VOCABULARY ==========")

for token in sorted(vocab):

    print(token)

print("\nVocabulary Size :", len(vocab))


# ============================================================
# STEP 11: TOKENIZE NEW WORD
# ============================================================

def tokenize_word(word, vocab):

    tokens = []

    while len(word) > 0:

        found = False

        for i in range(len(word), 0, -1):

            part = word[:i]

            if len(tokens) > 0:
                part = "##" + part

            if part in vocab:

                tokens.append(part)

                word = word[i:]

                found = True

                break

        if not found:

            return ["[UNK]"]

    return tokens


# ============================================================
# STEP 12: ADD UNKNOWN TOKEN
# ============================================================

vocab.add("[UNK]")


# ============================================================
# STEP 13: TEST WORD
# ============================================================

test_word = "hugs"

encoded_tokens = tokenize_word(
    test_word,
    vocab
)

print("\n========== TOKENIZATION ==========")

print("Input Word :", test_word)

print("Tokens :", encoded_tokens)


# ============================================================
# STEP 14: TOKEN IDs
# ============================================================

token_to_id = {}

for index, token in enumerate(sorted(vocab)):

    token_to_id[token] = index


token_ids = [
    token_to_id[token]
    for token in encoded_tokens
]


print("\n========== TOKEN IDs ==========")

print("Token to ID Mapping :")

for token, token_id in token_to_id.items():

    print(token, ":", token_id)


print("\nInput Tokens :", encoded_tokens)

print("Token IDs :", token_ids)


# ============================================================
# PROGRAM COMPLETED
# ============================================================

print("\n========== PROGRAM COMPLETED ==========")


# ============================================================
OUTPUT 
========== WORD FREQUENCIES ==========
hug : 3
hugs : 1
pug : 1
pugs : 1
bug : 1
bugs : 1
rug : 1
rugs : 1

========== INITIAL SPLITS ==========
hug -> ['h', '##u', '##g']
hugs -> ['h', '##u', '##g', '##s']
pug -> ['p', '##u', '##g']
pugs -> ['p', '##u', '##g', '##s']
bug -> ['b', '##u', '##g']
bugs -> ['b', '##u', '##g', '##s']
rug -> ['r', '##u', '##g']
rugs -> ['r', '##u', '##g', '##s']

========== INITIAL VOCABULARY ==========
##g
##s
##u
b
h
p
r

========== TOKEN FREQUENCIES ==========
h : 4
##u : 10
##g : 10
##s : 4
p : 2
b : 2
r : 2

========== PAIR FREQUENCIES ==========
('h', '##u') : 4
('##u', '##g') : 10
('##g', '##s') : 4
('p', '##u') : 2
('b', '##u') : 2
('r', '##u') : 2

========== WORDPIECE SCORES ==========
('h', '##u') : 0.1
('##u', '##g') : 0.1
('##g', '##s') : 0.1
('p', '##u') : 0.1
('b', '##u') : 0.1
('r', '##u') : 0.1

========== WORDPIECE TRAINING ==========

Merge 1
Best Pair : ('h', '##u')
Pair Frequency : 4
Score : 0.1
New Token : hu

Merge 2
Best Pair : ('p', '##u')
Pair Frequency : 2
Score : 0.166667
New Token : pu

Merge 3
Best Pair : ('b', '##u')
Pair Frequency : 2
Score : 0.25
New Token : bu

Merge 4
Best Pair : ('r', '##u')
Pair Frequency : 2
Score : 0.5
New Token : ru

Merge 5
Best Pair : ('hu', '##g')
Pair Frequency : 4
Score : 0.1
New Token : hug

========== FINAL WORD SPLITS ==========
hug -> ['hug']
hugs -> ['hug', '##s']
pug -> ['pu', '##g']
pugs -> ['pu', '##g', '##s']
bug -> ['bu', '##g']
bugs -> ['bu', '##g', '##s']
rug -> ['ru', '##g']
rugs -> ['ru', '##g', '##s']

========== FINAL VOCABULARY ==========
##g
##s
##u
b
bu
h
hu
hug
p
pu
r
ru

Vocabulary Size : 12

========== TOKENIZATION ==========
Input Word : hugs
Tokens : ['hug', '##s']

========== TOKEN IDs ==========
Token to ID Mapping :
##g : 0
##s : 1
##u : 2
[UNK] : 3
b : 4
bu : 5
h : 6
hu : 7
hug : 8
p : 9
pu : 10
r : 11
ru : 12

Input Tokens : ['hug', '##s']
Token IDs : [8, 1]

========== PROGRAM COMPLETED ==========
