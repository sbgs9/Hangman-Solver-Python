import requests
import json
from collections import Counter

def get_frequencies(length):
    words = open('words.txt', 'r')
    lines = words.readlines()
    freqs = Counter()
    for line in lines:
        if len(line.strip()) == length:
            freqs += Counter(line.strip())
    return freqs

def getFilteredFrequencies(length, doesnt_contain, contains):
    words = open('words.txt', 'r')
    lines = words.readlines()
    freqs = Counter()
    for line in lines:
        if len(line.strip()) == length:

            freqs += Counter(line.strip())
    return freqs


def main():
    url = 'https://hangman-api.herokuapp.com/hangman'
    x = requests.post(url)
    y = x.json()
    token = y["token"]
    word_length = len(y["hangman"])
    freqs = get_frequencies(length=word_length)
    contains = []
    doesnt_contain = []
    for letter, count in freqs.most_common():
        guess = requests.put(url, data={'token':token, 'letter': letter})
        print('Guess: ' + letter)
        resp = guess.json()
        print(resp)
        if resp['correct'] == False:
            doesnt_contain.append(letter)
            print('Guess was wrong')
            break
        elif resp['correct'] == True:
            contains.append(letter)
            print('Guess was correct')






if __name__ == '__main__':
    main()
