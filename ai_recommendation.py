def sortorder(numList, type):
    OrderedList = []
    length=len(numList)
    i = 0
    while i < len(numList):
        OrderedList.append("")
        i = i + 1
    if type == "D":
        i = 0
        while i < length:
            OrderedList[i] = min(numList)
            del numList[numList.index(min(numList))]
            i = i + 1
    elif type == "A":
        i = 0
        while i < length:
            OrderedList[i] = max(numList)
            del numList[numList.index(max(numList))]
            i = i + 1
    return OrderedList
from nltk.stem import PorterStemmer
import yake
porter = PorterStemmer()

def extracto(text):
    extractor=yake.KeywordExtractor(top=5, stopwords=None, n = 2)
    keywords = extractor.extract_keywords(text)
    keyword = []
    score = []
    for kw, v in keywords:
        score.append(float(v)) 
    score = sortorder(score, "A")
    for i in score:
        for x,y in keywords:
            if y == i:
                break
        keyword.append(porter.stem(x))
    return keyword
text1 = extracto("Cyber security refers to the practice of protecting computer systems, networks, and data from unauthorized access, theft, damage, or other types of cyber attacks. Cyber attacks can take many forms, including phishing, malware, ransomware, denial-of-service attacks, and hacking.")
print(text1)