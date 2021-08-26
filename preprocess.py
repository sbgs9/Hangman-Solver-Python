def to_lower():
    words = open('words.txt', 'r+')
    #new_words = open('words_processed.txt', 'r+')
    lines = words.readlines()
    for index in range(len(lines)):
        curr_word = lines[index].strip()
        lower_word = curr_word.lower()
        lines[index] = lower_word + '\n'
    return lines
        #new_words.write(lines[index] + '\n')

def remove_duplicates():
    uniqlines = set(to_lower())
    new_words = open('words_processed.txt', 'r+')
    for line in uniqlines:
        new_words.write(line)


def main():
    remove_duplicates()

if __name__ == "__main__":
    main()