from component import *
from model import *

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

print("ready to search")
while True:
    search_text = input("2018-22788> ")
    search_word = search_text.split()
    results = SearchM().search(search_word)
    for result in results:
        print("{0}, {1}, {2}, {3}".format(result["id"], result["title"], result["idf"], result["total_value"]) )