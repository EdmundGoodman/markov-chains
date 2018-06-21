//Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
//Markov chain text generator
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <fstream>
#include <sstream>
#include <random>

std::string getFileContents(char targetFile[]) {
  //Read contents of the given file into a string
  std::ifstream file( targetFile );
  std::stringstream buffer;
  buffer << file.rdbuf();
  std::string str = buffer.str();
  return str;
}

std::vector<std::string> splitString(std::string text) {
  //Split the string by spaces, to form a vector
  std::istringstream buf(text);
  std::istream_iterator<std::string> beg(buf), end;
  std::vector<std::string> tokens(beg, end);
  return tokens;
}

int generateRandomNumber(int start, int stop) {
  //Return a random number in the given range
  std::random_device rd;
  std::mt19937 eng(rd());
  std::uniform_int_distribution<> distr(start, stop);
  return distr(eng);
}

bool isEndOfSentence(std::string word) {
  //Return whether word is at the end of a sentence (if it ends with punctuation)
  char EOS[3] = {'.','!','?'};
  for (int i=0; i<3; i++) {
    if (word[-1] == EOS[i]) {
      return true;
    }
  }
  return false;
}


int main() {
  //Set initial variables
  int length = 100;

  //Read the contents of the file into a string
  char targetFile[] = "./corpus.txt";
  std::string text = getFileContents(targetFile);

  //Split the string into individual words my spaces
  std::vector<std::string> splitText = splitString(text);

  //Initialise and associative array to store the word, then all of the next words
  std::map <std::string, std::vector<std::string> > d;
  //Loop over the splitText array
  for(std::vector<std::string>::size_type count=0; count != splitText.size(); count++) {
    //If the associative array doesn't have a key of the current word:
    if (d.count( splitText[count] )) {
      //Initialise the array of all following words, then add it to the associative array
      std::vector<std::string> wordArray;
      wordArray.assign(1,splitText[count+1]);
      d[splitText[count]] = wordArray;
    } else {
      //Add the next word to the array of next words
      d[splitText[count]].push_back(splitText[count+1]);
    }
  }

  //Randomly choose a starting word from the start of a sentence, and start the chain
  std::string word = splitText[generateRandomNumber(0, splitText.size())];
  std::string chain = word + " ";

  //While the chain isn't too long, and there is an ongoing sentence
  while (splitString(chain).size() <= length && !isEndOfSentence(word)) {
    //Pick a new word, add it to the chain, than set the new word as the old word
    std::string nextWord = splitText[generateRandomNumber(0, splitText.size())];
    chain += (nextWord + " ");
    word = nextWord;
  }

  //Print the chain
  std::cout << chain << std::endl;

  return 0;
}
