from functools import partial
import nltk
import os
import json
import jsbeautifier
from pprint import pprint
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict
import ujson

def main():
  docIDtoURL = indexer() # constructs three partial inverted indexes and also returns a docIDtoURL dict

  # calls mergeIndex on each partial inverted index
  mergeIndex('d1.json')
  mergeIndex('d2.json')
  mergeIndex('d3.json')
      
  with open('docIDtoURL.txt', 'w', encoding='utf-8') as f:
      f.write(str(docIDtoURL)) # docIDtoURL dict



def importantText(soup: BeautifulSoup):
    importantList = []

    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()

    # finds all the important tokens that are bolded, in h1-h6, and the title
    for bold in soup.find_all("b"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(bold.text)]
      for token in stemTokens:
        importantList.append(token)

    for h1 in soup.find_all("h1"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(h1.text)]
      for token in stemTokens:
        importantList.append(token)

    for h2 in soup.find_all("h2"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(h2.text)]
      for token in stemTokens:
        importantList.append(token)

    for h3 in soup.find_all("h3"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(h3.text)]
      for token in stemTokens:
        importantList.append(token)
    
    for h4 in soup.find_all("h4"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(h4.text)]
      for token in stemTokens:
        importantList.append(token)
    
    for h5 in soup.find_all("h5"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(h5.text)]
      for token in stemTokens:
        importantList.append(token)

    for h6 in soup.find_all("h6"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(h6.text)]
      for token in stemTokens:
        importantList.append(token)

    for title in soup.find_all("title"):
      stemTokens = [ps.stem(token) for token in tokenizer.tokenize(title.text)]
      for token in stemTokens:
        importantList.append(token)

    return importantList

def mergeIndex(file):
  # opens partial index, and splits into 4 inverted indexes sorted alphabetically that are dumped to their own json files
  a_iDict = dict()
  j_rDict = dict()
  s_zDict = dict()
  digits_Dict = dict()

  a_iList = ['a','b','c','d','e','f','g','h','i']
  j_rList = ['j', 'k','l','m','n','o','p','q','r']
  s_zList = ['s','t','u','v','w','x','y','z']
  digitsList = ['0','1','2','3','4','5','6','7','8','9']

  if file == 'd1.json':
    with open(file, 'r', encoding='utf-8') as f:
        partialIndex = ujson.load(f)
        for k,v in partialIndex.items():
          if k[0] in a_iList:
            a_iDict[k] = v
          elif k[0] in j_rList:
            j_rDict[k] = v
          elif k[0] in s_zList:
            s_zDict[k] = v
          elif k[0] in digitsList:
            digits_Dict[k] = v
  else:
    with open(file, 'r', encoding='utf-8') as f:
      partialIndex = ujson.load(f)
      with open('a_i.json', 'r', encoding='utf-8') as a_i, open('j_r.json', 'r', encoding='utf-8') as j_r, open('s_z.json', 'r', encoding='utf-8') as s_z, open('digits.json', 'r', encoding='utf-8') as digits:
        a_iDict = ujson.load(a_i)
        j_rDict = ujson.load(j_r)
        s_zDict = ujson.load(s_z)
        digits_Dict = ujson.load(digits)
        for k,v in partialIndex.items():
          if k[0] in a_iList:
            if k in a_iDict:
              a_iDict[k].update(v)
            else:
              a_iDict[k] = v
          elif k[0] in j_rList:
            if k in j_rDict:
              j_rDict[k].update(v)
            else:
              j_rDict[k] = v
          elif k[0] in s_zList:
            if k in s_zDict:
              s_zDict[k].update(v)
            else:
              s_zDict[k] = v
          elif k[0] in digitsList:
            if k in digits_Dict:
              digits_Dict[k].update(v)
            else:
              digits_Dict[k] = v

  with open('a_i.json', 'w', encoding='utf-8') as f:
    ujson.dump({key:val for key, val in sorted(a_iDict.items(), key=lambda i:i[0])}, f)
  with open('j_r.json', 'w', encoding='utf-8') as f:
    ujson.dump({key:val for key, val in sorted(j_rDict.items(), key=lambda i:i[0])}, f)
  with open('s_z.json', 'w', encoding='utf-8') as f:
    ujson.dump({key:val for key, val in sorted(s_zDict.items(), key=lambda i:i[0])}, f)
  with open('digits.json', 'w', encoding='utf-8') as f:
    ujson.dump({key:val for key, val in sorted(digits_Dict.items(), key=lambda i:i[0])}, f)

def indexer():
  docID = 0 
  index = dict() # {token: {docID: [freq, importantWeight]}}
  docIDtoURL = dict() # {docID: url}

  ps = PorterStemmer() # stemming

  filesCounter = 1
  indexCounter = 0 

  # iterates through every file in every directory inside the DEV directory (each file is a webpage)
  for (root, dirs, files) in os.walk('DEV', topdown=True):
    for file in files:
      if indexCounter > 2:
        return docIDtoURL
      with open(os.path.join(root, file), encoding='UTF-8') as json_file:
        data = ujson.load(json_file)

      url = data['url']
      content = data['content']

      # using lxml parser in BeautifulSoup to extract content
      soup = BeautifulSoup(content, 'lxml')
      text = soup.getText()
      # using nltk tokenizer to extract all tokens
      tokenizer = RegexpTokenizer(r'\w+')
      tokens = tokenizer.tokenize(text)

      importantTokens = importantText(soup) # returns a list of tokens that are important

      # goes through every token, stems it using PorterStemmer and checking if its important, then store it in the inverted index as the key, 
      # and the value as a dict with its key as the docID and value as postings [freq, importantWeight
      # also creates another dict that holds the docID as the key and the url as the value
      for token in tokens:
        stemToken = ps.stem(token)
        score = 0
        if stemToken in importantTokens:
          score = 5

        if stemToken in index and docID in index[stemToken]:
          index[stemToken][docID][0] += 1
        elif stemToken in index:
          index[stemToken][docID] = [1, score]
        else:
          index[stemToken] = {docID: [1, score]}

        docIDtoURL[docID] = url 

        # splits corpus into three inverted indexes, which are off-loaded into their own json files
        if filesCounter == 18464 and indexCounter <= 1:
          if indexCounter == 0:
            with open("d1.json", 'w', encoding='utf-8') as f:
              ujson.dump(index, f)
              index.clear()
              filesCounter = 0
              indexCounter += 1
            
          elif indexCounter == 1:
            with open("d2.json", 'w', encoding='utf-8') as f:
              ujson.dump(index, f)
              index.clear()
              filesCounter = 0
              indexCounter += 1
          
        elif indexCounter == 2 and filesCounter == 18465:
          with open("d3.json", 'w', encoding='utf-8') as f:
            ujson.dump(index, f)

          filesCounter = 0

      docID += 1
      filesCounter += 1

  return docIDtoURL


if __name__ == "__main__":
  main()
