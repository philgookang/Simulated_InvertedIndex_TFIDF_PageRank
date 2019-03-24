from component import *

'''
    Setup database
    -> remove any old tables
    -> create required tables
    -> added indexes to each table 
'''
Setup()

'''
    Initalize database
    -> calcuate inverted indexes
    -> term frequency
    -> inverted term frequency
    -> page rank
'''
Initalize()

while True:
    search_text = input("2018-22788> ")
    search_word = search_text.split()

    for word in search_word:
        result = []