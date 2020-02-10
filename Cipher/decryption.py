import numpy as np
from pathlib import Path
from collections import Counter
import random as rand


def generate_freq(path):
    # Access and read file
    root = Path(".")
    path = root / path
    path.exists()

    with path.open(mode='r') as file:
        content = file.read()

    content = content.upper()
    count = Counter(content).most_common()

    letter_frequencies = ' '
    for item in count:
        if isinstance(item[0], str) and ord(item[0]) < 91 and ord(item[0]) > 64:
            letter_frequencies += item[0]
    return letter_frequencies


def freq_analysis(encoded, frequencies):
    encoded = encoded.upper()
    count = Counter(encoded).most_common()

    test_freq = ''
    for item in count:
        test_freq += item[0]

    decoded = ''
    for letter in encoded:
        index = test_freq.find(letter)
        decoded += frequencies[index]

    return decoded


def prob_matrix(path):
    # Access and read file
    root = Path(".")
    path = root / path
    path.exists()

    with path.open(mode='r') as file:
        content = file.read()

    content = content.upper()

    freq = np.zeros((27, 27))

    # Establish an initial out-of-range last index
    last_idx = -1

    # loop through the content (War and Peace) and record the frequency of letter pairs
    for item in content:

        # Note: the ord() function returns the ASCII value of the explicit parameter
        if ord(item) < 91 and ord(item) > 64:
            idx = ord(item) - 64  # subtracts 64 so the characters A-Z have indeces starting at 1
            if last_idx is not -1:
                freq[last_idx][idx] += 1  # Increment the frequency of the letter pair by one
            last_idx = idx  # Reset the last index to the current index before looping again

        # Separate case for spaces, which have an ASCII value of 32
        if ord(item) is 32:
            idx = 0;  # the index for spaces is 0 in the probability matrix
            if last_idx is not -1:
                freq[last_idx][idx] += 1  # Increment the frequency of the letter pair by one
            last_idx = idx  # Reset the last index to the current index before looping again

    sum = np.sum(freq, axis=0)  # Sum the frequencies for each starting letter (each row)

    # Divide each row of frequencies by the corresponding sum to obtain a matrix of probabilities
    for index in range(27):
        freq[index] /= sum[index]

    # add a very small value to the matrix so there are no zeros - zeros are problamatic when we need to
    # multiply probabilities (multiplying by zero immediately zeros everything out)
    adjust = np.zeros((27, 27)) + 1E-7
    freq += adjust

    return freq


# decodes the given code using the given probability matrix, running through
# the Markov chain Monte Carlo algorithm n times
def markov_chain(code, prob_mat, n):
    last_prob = -1  # Establish an initial impossible last probability

    # Iterate the algorithm n times
    for _ in range(n):
        # if (last_prob is not -1 and curr_prob > 1E-200):
        # return code

        # Generate 2 random ASCII values
        idx1 = rand.randint(65, 91)
        if idx1 is 91:  # 91 is not a letter, but I use it to represent a space
            idx1 = 32  # ASCII value of a space
        idx2 = rand.randint(65, 91)
        if idx2 is 91:
            idx2 = 32

        # Switch the two letters indicated by the ASCII values in the string to create a modified code
        new_code = ''
        for letter in code:
            if letter is chr(idx1):
                new_code += chr(idx2)
            elif letter is chr(idx2):
                new_code += chr(idx1)
            else:
                new_code += letter

        last_idx = -1
        curr_prob = 1

        for letter in new_code:
            if ord(letter) > 64 and ord(letter) < 91:
                idx = ord(letter) - 64
            elif letter is ' ':
                idx = 0
            if last_idx is not -1:
                curr_prob *= prob_mat[last_idx][idx]
            last_idx = idx

        if curr_prob > last_prob:
            code = new_code
            last_prob = curr_prob
        elif curr_prob < last_prob and rand.random() < curr_prob / last_prob:  # if it's not better, update it sometimes
            code = new_code
    print(curr_prob)
    return code

frequencies = generate_freq('source_text/warandpeace.txt')

war_prob = prob_matrix('source_text/warandpeace.txt')

code="ONTI JI HNT XADZVT AU NDBPI TGTIHV JH YTXABTV ITXTVVPZC UAZ AIT STASET HA WJVVAEGT HNT SAEJHJXPE YPIWV ONJXN NPGT XAIITXHTW HNTB OJHN PIAHNTZ PIW HA PVVDBT PBAIK HNT SAOTZV AU HNT TPZHN"

decryption = markov_chain(freq_analysis(code, frequencies), war_prob, 5000)
