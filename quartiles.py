#file -- quartiles.py --
''' Python module to take an input list of strings, where each 
    string is a grouping of letters and returns a list of English 
    words that can be formed by concatinating any permutations of 
    4 or less strings from the input list. 
'''

import sys
import itertools
import random
import sqlite3


def check_value_exists(cursor, value):
    cursor.execute("SELECT 1 FROM Words WHERE word = ?", (value,))
    result = cursor.fetchone()
    return result is not None

def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in itertools.product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

def containsVowel(word):
    vowels = {"a", "e", "i", "o", "u", "y"}
    if any(char in vowels for char in word.lower()):
        return True
    else:
        return False

def concatinateTuple(tuple):
    segment = ''
    for element in tuple:
        segment = segment + element
    return segment


def getWords(gridList):
   if (len(gridList) < 4):
       return ([],0)

   source = sqlite3.connect("dictionary.db")
   conn = sqlite3.connect(':memory:')
   source.backup(conn)
   cursor = conn.cursor()

   count = 0
   wordList = []
   for length in [1,2,3,4]:
       mylist = list(permutations(gridList,length))
       for element in mylist:
          potentialWord = concatinateTuple(element)
          count += 1
          if check_value_exists(cursor, potentialWord) and containsVowel(potentialWord):
             wordList.append(potentialWord)

   wordList = list(set(wordList))
   wordList.sort()
   return (wordList,count)

if __name__ == "__main__":
    my_list = ["cata","cly","sm","ic","co","ndo","mini","um","poc","ket","kni","fe","scr","ut","in","ize","cul","tiv","at","ed"]
    (words,count) = getWords([x.upper() for x in my_list])
    print(words)
    print(count)
