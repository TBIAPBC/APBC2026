import argparse
import re

def WordCount(filename,l,I):
    word_dict=dict()
    total_word_list=list()
    
    with open (filename) as f:
        text=f.read()
           
    words=re.split(r"[^\w]+",text)

    for word in words:
        if word:
            if I: 
                total_word_list.append(word.lower())
            else:
                total_word_list.append(word)
    
    for w in total_word_list:
        if w in word_dict:
            word_dict[w]=word_dict[w]+1
        else:
            word_dict[w]=1
                
    sorted_dict=dict(sorted(word_dict.items(), key=lambda item: (-item[1], item[0])))
    
    if l:    
        for i in sorted_dict:
            print(f'{i} {sorted_dict[i]}')
    else:
            print(f'{len(sorted_dict)} / {len(total_word_list)}')
    
    return ()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Counts words in input files")
    parser.add_argument("filename", help="Input file")
    parser.add_argument("-l", action="store_true", help="prints a list instead of only counts. List is sorted by word frequency, in descending order. In case of equal frequencies order is alphabetical")
    parser.add_argument("-I", action="store_true", help="Ignore case")

    args = parser.parse_args()

    WordCount(args.filename, l=args.l, I=args.I)