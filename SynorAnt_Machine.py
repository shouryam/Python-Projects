import nltk
from nltk.corpus import wordnet
word = str(input("Enter the word you want the Synoym or antonym of: "))
x =2
while(x != 0 and x != 1):
    x = int(input("Enter 1 for Antonyms or 0 for Synonyms: "))

print("Definition of " + word + ":")
syn = wordnet.synsets(word)
print(syn[0].definition())
if x == 1:
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    print(antonyms)
else:
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    print(synonyms)