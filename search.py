from indexer import *
import ast
import math
import time
import ujson as json

numDocs = 55393

def runTextInterface():
  with open(r'docIDtoURL.txt', 'r', encoding='utf-8') as f:
    docIDtoURL = ast.literal_eval(f.read())

  while(True):
    # start of search interface; to quit, enter an empty query
    query = input("Enter search query (or an empty query to quit): ")
    start_time = int(round(time.time() * 1000)) # start of timer
    if query == '':
      return

    sortedDict_docId = getRankedURLs(query)
    if sortedDict_docId == False:
      continue
    else:
      outputURL(sortedDict_docId, docIDtoURL) # outputs search results
      end_time = int(round(time.time() * 1000)) # end of timer
      time_lapsed = end_time - start_time
      print(f'{time_lapsed}ms')

def computeTf_Idf(index, token, docID):
  df = len(index[token])
  idf = (math.log(numDocs, 10) / df)
  tf = index[token][docID][0]
  tf_w = 1 + (math.log(tf, 10))
  importantWeight = index[token][docID][1]

  tf_idf = tf_w * idf + importantWeight
  return tf_idf

def outputURL(sortedDict_docId, docIDtoURL):
    str = ''
    for docID in sortedDict_docId:
      str += docIDtoURL[int(docID)]
      str += '\n'
    
    if len(str) == 0:
      print("No results found")
    else:
      print('Search results: ')
      print(str[:-1])


def getRankedURLs(query):
    # goes through every token in search query, and computes the tf-idf score for each token, which is stored in a dict as a value with its key as the docID
    a_iList = ['a','b','c','d','e','f','g','h','i']
    j_rList = ['j', 'k','l','m','n','o','p','q','r']
    s_zList = ['s','t','u','v','w','x','y','z']
    digitsList = ['0','1','2','3','4','5','6','7','8','9']

    list_of_tokens = tokenizeQuery(query) # tokenizes search query and returns a list of tokens
    list_of_docIDs = []
    list_of_dicts = []
    docIDtoScore = dict()

    if len(list_of_tokens) == 0:
      print(f"Your search - '{query}' - did not match any documents")
      return False

    for token in list_of_tokens:
      try:
        if token[0] in a_iList:
          with open('a_i.json', 'r', encoding='utf-8') as f:
            a_iIndex = json.load(f)
            list_of_dicts.append(a_iIndex[token])
            list_of_docIDs.append(set(a_iIndex[token].keys()))
        elif token[0] in j_rList:
          with open('j_r.json', 'r', encoding='utf-8') as f:
            j_rIndex = json.load(f)
            list_of_dicts.append(j_rIndex[token])
            list_of_docIDs.append(set(j_rIndex[token].keys()))
        elif token[0] in s_zList:
          with open('s_z.json', 'r', encoding='utf-8') as f:
            s_zIndex = json.load(f)
            list_of_dicts.append(s_zIndex[token])
            list_of_docIDs.append(set(s_zIndex[token].keys()))
        elif token[0] in digitsList:
          with open('digits.json', 'r', encoding='utf-8') as f:
            digitsIndex = json.load(f)
            list_of_dicts.append(digitsIndex[token])
            list_of_docIDs.append(set(digitsIndex[token].keys()))
        else:
            print(f"Your search - '{query}' - did not match any documents")
            return False
      except KeyError:
        print(f"Your search - '{query}' - did not match any documents")
        return False

      
    list_of_all_docIDs = list_of_docIDs[0].intersection(*list_of_docIDs) # intersects all docIDs that contains every token in search query

    for docID in list_of_all_docIDs:
      for token in list_of_tokens:
        if token[0] in a_iList:
          score_per_token = computeTf_Idf(a_iIndex, token, docID)
        elif token[0] in j_rList:
          score_per_token = computeTf_Idf(j_rIndex, token, docID)
        elif token[0] in s_zList:
          score_per_token = computeTf_Idf(s_zIndex, token, docID)
        elif token[0] in digitsList:
          score_per_token = computeTf_Idf(digitsIndex, token, docID)
        if docID in docIDtoScore:
          docIDtoScore[docID] += score_per_token
        else:
          docIDtoScore[docID] = score_per_token

    sortedDict = dict(sorted(docIDtoScore.items(), key = lambda item: item[1], reverse=True)) # sorts docIDtoScore dict by tf-idf score in order to get the top ten URLs

    return sortedDict

      
def outputURL(list_of_docIDs, docIDtoURL):
    counter = 1
    str = ''
    for docID in list_of_docIDs:
      if counter == 11:
        break
      str += f'{counter}. {docIDtoURL[int(docID)]}'
      str += '\n'
      counter += 1
    
    if len(str) == 0:
      print("No results found")
    else:
      print('Search results: ')
      print(str[:-1])


def tokenizeQuery(str):
  list_of_tokens = []
  ps = PorterStemmer()
  tokenizer = RegexpTokenizer(r'\w+')
  stopWords = set(stopwords.words('english'))

  tokens = tokenizer.tokenize(str)

  stopWordsCounter = 0
  tokensCounter = 0

  for token in tokens:
    if token in stopWords:
      stopWordsCounter += 1
    tokensCounter += 1
  if stopWordsCounter / tokensCounter >= .75:
    for token in tokens:
      stemToken = ps.stem(token)
      list_of_tokens.append(stemToken)
  else:
    for token in tokens:
      if token not in stopWords:
        stemToken = ps.stem(token)
        list_of_tokens.append(stemToken)

  return list_of_tokens

if __name__ == "__main__":
  runTextInterface()