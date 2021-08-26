import requests
import json
from collections import Counter

# gets base frequency list. Returns Counter object
def get_frequencies(length):
    words = open('words_processed.txt', 'r')
    lines = words.readlines()
    freqs = Counter()
    for line in lines:
        if len(line.strip()) == length:
            freqs += Counter(line.strip())
    return freqs

# gets filtered list of letters. Returns Counter object
def get_filtered_frequencies(length, doesnt_contain, contains):
    words = open('words_processed.txt', 'r')
    lines = words.readlines()
    freqs = Counter()
    if len(doesnt_contain) != 0 and len(contains) == 0:
        for line in lines:
            if len(line.strip()) == length and not any(letter in line.strip() for letter, count in doesnt_contain):
                freqs += Counter(line.strip())
    elif len(doesnt_contain) != 0 and len(contains) != 0:
        for line in lines:
            if len(line.strip()) == length and any(letter in line.strip() for letter, count in contains) and not any(letter in line.strip() for letter, count in doesnt_contain):
                for letter,count in contains:
                    if num_occurrances(line.strip(), letter) == count:
                        freqs += Counter(line.strip())
    return freqs
# gets the number of occurrances of a letter in a word
# returns the count as an integer    
def num_occurrances(word, letter):
    count = 0
    for char in word:
        if char == letter:
            count += 1
    return count

# gets the indices of all of the occurrances of a letter in a word
# returns a list of the indices of the occurrances of the letter in the word
def get_indices(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]

# main driver
def main():
    url = 'https://hangman-api.herokuapp.com/hangman'
    x = requests.post(url)
    y = x.json()
    token = y["token"]
    word_length = len(y["hangman"])
    freqs = get_frequencies(length=word_length)
    contains = []
    doesnt_contain = []
    num_incorrect = 0
    word_preview = ''
    for num in range(word_length):
        word_preview += '_'
 
    while num_incorrect != 7:
        if '_' not in word_preview:
            break
        updated_freqs = get_filtered_frequencies(word_length, doesnt_contain, contains)
        if num_incorrect == 0:
            updated_freqs = freqs
        for letter, count in updated_freqs.most_common():
            if letter in contains:
                continue
            if '_' not in word_preview:
                break
            guess = requests.put(url, data={'token':token, 'letter': letter})
            print('Guess: ' + letter)
            resp = guess.json()
            if resp['correct'] == False:
                doesnt_contain.append((letter, 0))
                num_incorrect += 1
                break
            elif resp['correct'] == True:
                contains.append((letter, len(get_indices(resp['hangman'], letter))))
                for index in get_indices(resp['hangman'], letter):
                    word_preview = word_preview[:index] + letter + word_preview[index+1:]
            print(word_preview)

    data = requests.get(url, {'token':token})
    sol = data.json()['solution']
    if num_incorrect == 7:
        print("Guess we couldn't solve this one! We'll get it next time!")
        print('The solution was: ' + sol)
    else:
        print('WE GOT IT! THE CORRECT WORD IS: ' + word_preview)
        print('The solution was: ' + sol)
        

if __name__ == '__main__':
    main()
