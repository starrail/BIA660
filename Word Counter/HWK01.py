"""
Senti Words
assignment 1
"""

import time


def run(file, posFile):
    """
    find the word that appears most frequently right after a positive word from a file
    :param file: the path to a text file
    :param posFile: the path to a file with positive words
    :return: the word that appears most frequently right after a positive word
    """
    # load data
    posWords = set(line.strip() for line in open(posFile))
    fr = open(file)

    # creat a dict to count words right after a positive word
    fre = {}

    # searching every line in this file
    for line in fr:
        # creat a list to contain every words in this line
        # turn these words into lower case
        words = line.lower().strip().split(' ')

        # find the index of positive words from the list
        for i in range(len(words)-1):
            if words[i] in posWords:
                # find the word right after the positive words
                # count the frequency of the word right after positive words
                if words[i+1] in fre:
                    fre[words[i+1]] += 1
                else:
                    fre[words[i+1]] = 1

    fr.close()

    # iterate over the dict, find the most frequently right after a positive word
    ans = []
    for key, value in fre.items():
        if value == max(fre.values()):
            ans.append(key)

    return ', '.join(ans)


if __name__ == '__main__':
    start = time.time()

    file = '/Users/yaoyuchen/Desktop/WebMining/senti/uuuu.txt'
    positive_words = '/Users/yaoyuchen/Desktop/WebMining/senti/positive-words.txt'
    print(run(file, positive_words))

    print(f"time span: {(time.time()) - start} s")
