#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
#Markov chain text generator
import re, random, math

class analyseText:
    def __init__(self, value):
        self.value = value

    def getMarkovChain(self, length=100, endOfSentence=list('.?!')):
        splitText = [w for w in self.value.replace("\n","").split(" ") if w != '']
        d = {}
        for count,word in enumerate(splitText[:-1]):
            try:
                d[word] = d[word] + [splitText[count+1]]
            except KeyError:
                d[word] = [splitText[count+1]]

        word, chain, count = random.choice(splitText), "", 0

        while count <= length or word[-1] not in endOfSentence:
            try:
                nextWord = random.choice(d[word])
            except KeyError:
                nextWord = random.choice(splitText)
            chain += nextWord+" "
            word = nextWord
            count += 1

        return chain[0].upper() + chain[1:-1]

def getText(targetFile):
    with open(targetFile, "rt", encoding="utf-8") as f:
        return f.read()

targetFile = str(input("Target file: "))
corpusText = getText(targetFile)
t = analyseText(corpusText)
markovChain = t.getMarkovChain()
print(markovChain)
