import sys
import re



def get_words(text):
    words = [w for w in re.split(r'[ \.\,\[\]\!\'\-\"\;\?\:\n\t]+', text) if w] #had to add the if w because otherwise and empty string "" is produced at the end of the text
    return words


def ignore(words):
    ignored_list = []
    for word in words:
        ignored_word = word.lower() 
        ignored_list.append(ignored_word)
    return ignored_list

def sorting_function(elem):
    return elem[1]*-1, elem[0]

def unique_words_f(words):
    unique_words_list = []
    dict_word_count = {}
    bob = []


    for word in words:
        if word not in unique_words_list:
            unique_words_list.append(word)
        dict_word_count[word] = dict_word_count.get(word, 0) + 1

    for key, value in dict_word_count.items():
        bob.append([key, value])

    sorted_bob = sorted(bob, key=sorting_function)
    
    
    return sorted_bob, dict_word_count   


def l(words):
    unique_words_count_list = unique_words_f(words)[0]
    for element in unique_words_count_list:
        word = element[0]
        count = element[1]
        print(f"{word}\t{count}")


    

def main():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        text = f.read()
    words = get_words(text) 
    if "-I" in sys.argv:
        words = ignore(words)
    unique_words = unique_words_f(words)[0]    
    total_word_count = len(words)
    unique_word_count = len(unique_words)

    if "-l" in sys.argv:
        l(words)

    else:    
        print(f"{unique_word_count} / {total_word_count}")

    

if __name__ == "__main__":
    main()




