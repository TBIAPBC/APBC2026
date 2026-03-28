#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <algorithm>
using namespace std;


//reads file 
string read_file(const string& filename) { 
    
    ifstream file(filename); //open the file

    //check if it is opened
    if (!file.is_open()) {
        cerr << "Error: file could not be opened!" << endl;
        return "";
    }

    //read file to string
    string content((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());

    file.close(); //close file

    return content;
}

//identifies words in content of file and stores them in a vector
vector<string> content_to_vector(string& content) { 

    vector<string> words;
    string current_word;

    for (int i = 0; i < content.size(); i++) { //identify words
        char c = content[i];
        if (isalpha(c)) {
            current_word += c;
        } else if (current_word.size() > 0) {
            words.push_back(current_word);
            current_word = "";
        }
    }
    if (current_word.size() > 0) { 
        words.push_back(current_word);
    }
    return words;
}


//converts uppercase letters to lowercase
vector<string> convert_uppercase(vector<string> words) { 

    for (string& word : words) { //iterates over words
        for (char& c: word) {
            c = tolower(c); //converts c to lowercase, if it is already lowercase, it returns the identical char
        }
    }
    return words;
}


// generate map containing words and their count 
map<string, int> count_words(vector<string> words) {

    map<string, int> counts;

    for(const string& word : words) {
        counts[word]++;
    }
    return counts;
}


//function that sorts words by counts and alphabet using bubble sort
vector<pair<string, int>> sort_words(map<string, int> counts) {

    vector<pair<string, int>> sorted(counts.begin(), counts.end()); //write words from map to vector

    for (int i = 0; i < sorted.size(); i++) {
        for (int j = 0; j < sorted.size() - 1; j++) {
            bool larger_count = sorted[j].second < sorted[j + 1].second; // larger count 
            bool prior_alphabet = sorted[j].second == sorted[j + 1].second && sorted[j].first > sorted[j + 1].first; //same count, but prior in alphabet
            
            //if either condition is true, change places
            if (larger_count || prior_alphabet) { 
                pair<string, int> current = sorted[j];
                sorted[j] = sorted[j + 1];
                sorted[j + 1] = current;
            }
        }
    }
    return sorted;
}



int main(int argc, char* argv[]) {

    string filename = "";
    string output_file = "";
    bool ignore_case = false;
    bool list_words = false;

    //iterate over command line arguments and stores them in corresponding variable 
    for (int i = 1; i < argc; i++) {
        string arg = argv[i];
        if (arg == "-I") {
            ignore_case = true;
        } else if (arg == "-o" && i +1 < argc) {
            output_file = argv[i + 1];
            i++; 
        } else if (arg == "-l") {
            list_words = true;
        } else {
            filename = arg;
        }
    }

    // no input file given
    if (filename.empty()) {
        cerr << "Usage: " << argv[0] << " [-I] [-l] <filename>" << endl;
        return 0; 
    }

    // input file is empty 
    string content = read_file(filename);
    if (content.empty()) {
        cout << "Empty file!"; 
        return 0;
    }

    
    vector<string> words = content_to_vector(content);

    // if "-I" is given
    if (ignore_case) {
        words = convert_uppercase(words);
    }

    map<string, int> counts = count_words(words);

    int total_words = words.size();
    int different_words = counts.size();

    ostream& out = cout;
    ofstream fout;

    if (!output_file.empty()) { 
        fout.open(output_file); // open output file
        if (!fout.is_open()) { 
            cerr << "Error: could not open output file!" << endl;
            return 0;
        }
    }

    ostream& output = output_file.empty() ? cout : fout;

    // if "-l" is given
    if (list_words) { 
        vector<pair<string, int>> list = sort_words(counts);
        for (const pair<string, int>& entry: list) {
            output << entry.first << " " << entry.second << endl;
        }
    } else { // if "-l" is not given 
        output << different_words << " / " << total_words << endl;
    }


    return 0;
}