import json

def main():
  searchIndex()

def searchIndex():
  with open('a_i.json', 'r', encoding='utf-8') as f:
    a_iIndex = json.load(f)
  with open('j_r.json', 'r', encoding='utf-8') as f:
    j_rIndex = json.load(f)
  with open('s_z.json', 'r', encoding='utf-8') as f:
    s_zIndex = json.load(f)
  with open('digits.json', 'r', encoding='utf-8') as f:
    digitsIndex = json.load(f)

  bookKeepDict = dict()
  postingsDict = dict()
  
  with open('a_iIndex.txt', 'w', encoding='utf-8') as f:
    a_i_items = a_iIndex.items()
    #counter = 0
    #lengthItems = len(a_i_items)
    for k,v in a_i_items:
      postingsDict[k] = {}
      bookKeepDict[k] = f.tell()
      f.write(f'{k}:')
      for ik,iv in v.items(): # v = {docID: [freq, importantWeight]}
        postingsDict[k][ik] = f.tell()
        f.write(f'{ik} {iv[0]} {iv[1]},')
      #counter += 1
      f.write('\n')
    


  with open('j_rIndex.txt', 'w', encoding='utf-8') as f:
    for k,v in j_rIndex.items():
      postingsDict[k] = {}
      bookKeepDict[k] = f.tell()
      f.write(f'{k}:')

      for ik,iv in v.items():
        postingsDict[k][ik] = f.tell()
        f.write(f'{ik} {iv[0]} {iv[1]},')
      f.write('\n')

  with open('s_zIndex.txt', 'w', encoding='utf-8') as f:
    for k,v in s_zIndex.items():
      postingsDict[k] = {}
      bookKeepDict[k] = f.tell()
      f.write(f'{k}:')

      for ik,iv in v.items():
        postingsDict[k][ik] = f.tell()
        f.write(f'{ik} {iv[0]} {iv[1]},')
      f.write('\n')
  
  with open('digitsIndex.txt', 'w', encoding='utf-8') as f:
    for k,v in digitsIndex.items():
      postingsDict[k] = {}
      bookKeepDict[k] = f.tell()
      f.write(f'{k}:')

      for ik,iv in v.items():
        postingsDict[k][ik] = f.tell()
        f.write(f'{ik} {iv[0]} {iv[1]},')
      f.write('\n')
    

  
  with open('bookKeepIndex.json', 'w', encoding='utf-8') as f:
    json.dump(bookKeepDict, f)

  with open('postingsIndex.json', 'w', encoding='utf-8') as f:
    json.dump(postingsDict, f)

if __name__ == "__main__":
  main()