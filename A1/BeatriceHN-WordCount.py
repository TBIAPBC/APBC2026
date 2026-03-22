import argparse
import regex

def CountWords(file, ignore_case=False, list=False):
    if ignore_case:
        file = file.lower()
    clean_text = regex.sub(r'[^\p{L}\p{N}\s]', ' ', file)
    word_list = clean_text.split()
    word_count = {'total': 0}
    for word in word_list:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
        word_count['total'] += 1
    if list:
        word_list = sorted(word_count.items(), key=lambda item: (-item[1], item[0]))
        for word, count in word_list:
            print(f"{word} {count}")
        return 
    return print(f'{len(word_count)} / {word_count['total']}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r', encoding='utf-8'), help='File with written text to count words in.')
    parser.add_argument('-I', '--ignore_case', help='Ignore case when counting words.', action='store_true')
    parser.add_argument('-l', '--list', help='List all words and their counts.', action='store_true')
    args = parser.parse_args()

    file = args.file.read()
    CountWords(file, ignore_case=args.ignore_case,  list=args.list)