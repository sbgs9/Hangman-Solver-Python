def to_lower():
    words = open('words.txt', 'w+')
    lines = words.readlines()
    for line in lines:
        curr_word = line.strip()
        lower_word = curr_word.lower()
        line = lower_word

def remove_duplicates():
    uniqlines = set(open('words.txt').readlines())
    new_words = open('newwords.txt', 'w+')
    new_words.writelines(set(uniqlines))
    new_words.close()

def main():
    to_lower()

if __name__ == "__main__":
    main()