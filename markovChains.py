#Markov chain text generator
import random
import numpy as np

class MarkovChain:
    def __init__(self, text):
        self.text = text

    def generateMarkovChain(self, length=100, EOS=list('.?!'), maxChunkWords=3, probability=1):
        """Generate a markov chain of words of a given lenth"""
        #Split the corpus text up by spaces
        splitText = [w for w in self.text.replace("\n"," ").split(" ") if w != '']
        #If the corpus text is too short, exit
        if len(splitText) < 1+maxChunkWords:
            raise Exception("Corpus text too short")

        #If their is no punctuation in the corpus text, exit
        if not any(x for x in splitText if x[-1] in EOS):
            raise Exception("No punctuation in the corpus text")

        #Generate a dictionary of words against a list of the list of all the next 2 words
        d = {}
        for count,word in enumerate(splitText[:-maxChunkWords]):
            try:
                #If the word is already in the dictionary
                for i in range(maxChunkWords):
                    d[word][i].append(splitText[count+(i+1)])
            except KeyError:
                #Otherwise, add a new dictionary entry
                d[word] = [[splitText[count+(i+1)]] for i in range(maxChunkWords)]


        #Generate the chain based on the dictionary
        chain = ""
        #Choose a starting word at the beginning of the sentence, if there is a full sentence
        word = random.choice([splitText[i] for i in range(len(splitText)) if splitText[i-1][-1] in EOS])

        #Until the chain is too long, and the sentence has ended
        while len(chain.split(" ")) <= length or word[-1] not in EOS:
            #Use a binomial probability to randomly generate the number of words per chunk
            actualChunkWords = int(np.random.binomial(maxChunkWords-1, probability, 1))+1
            #Chose a random index from the first next word list to pick from
            chosenWordIndex = random.randint(0, len(d[word][0])-1)
            #Generate the chunk of words, of length actualChunkWords, from the chosenWordIndex
            chosenWords = [d[word][i][chosenWordIndex] for i in range(actualChunkWords)]
            #Add the chunk to the chain
            chain += " ".join(chosenWords)+" "
            #Set the last word of the chunk as the key for the next chunk
            word = chosenWords[-1]

        #Return the chain, with a capitalised 1st letter
        return chain[0].upper() + chain[1:-1]

def getText(targetFile):
    """Return a string containing the contents of the target file"""
    with open(targetFile, "rt", encoding="utf-8") as f:
        return f.read()

if __name__=="__main__":
    #Generate the chain
    filename = "../corpus.txt" #str(input("Target file: "))
    text = getText(filename)
    t = MarkovChain(text)
    chain = t.generateMarkovChain(100, list('.?!'), 3, .5)
    print(chain)
