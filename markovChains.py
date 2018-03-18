#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
#Object orientatated markov chain (stochastic text generator)
import os, sys, re, random, pickle

class text(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.fileText = self.getText()
        self.chain = ""

    def getText(self):
        with open(self.fileName, "rt", encoding="utf-8") as f:
            return f.read()

    def getMarkovChain(self, chainLength=10, IWR=[r"\d\d\d:\d\d\d"], EOS=['.', '?', '!']):
        def isValidWord(word):
            #Abstraction of validation of word i.e. remove links
            for regex in IWR:
                if re.match(regex, word): return False
            return True

        def isChainFinished(chain, word):
            #Abstraction of the end conditions of the chain
            if (len(chain) > chainLength) and (word[-1] in EOS): return True
            return False

        #Get the words to base chain upon
        words = [w for w in self.fileText.split(" ") if isValidWord(w) and w != '']

        #Build the dictionary, using words from the corpus text
        d = {}
        for i, word in enumerate(words):
            try:
                second = words[i+1]
            except IndexError:
                break
            if word not in d:
                d[word] = []
            d[word].append(second)


        #Use the dictionary to randomly generate a chain
        previousWord = random.choice([key for key in d.keys() if key[0][0].isupper()])
        chain = [previousWord]
        while True:
            word = random.choice(d[previousWord])
            chain.append(word)
            if isChainFinished(chain, word):
                break
            previousWord = word

        return " ".join(chain)

os.system('clear')
targetFile = str(input("Target file: "))
corpusText = text(targetFile)
chain = corpusText.getMarkovChain(100)
print(chain)
