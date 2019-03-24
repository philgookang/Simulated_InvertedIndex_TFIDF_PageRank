from model import *
from component.PageRank import PageRank
from component.Tfidf import Tfidf
import nltk, time

class Initalize:

    def __init__(self):

        print("building tables...")

        offset = 0 # pagination offset
        limit = 100 # number of items to load per page

        while True: # create inverted index for each wiki

            # get list of wiki
            wiki_list = WikiM().getList(limit=limit, offset=(limit * offset))

            # check if list is empty
            if not len(wiki_list): break

            # loop through wiki list
            for wiki in wiki_list:

                start = time.time()

                # get tokenized word
                tokenized_word = nltk.tokenize.word_tokenize(wiki["text"])

                # create inverted index
                Tfidf(wiki, tokenized_word).create_inverted_index()

                # calcuate tf, idf, tfidf
                Tfidf(wiki, tokenized_word).create_term_frequency()
                #break
            #break

            offset = offset + 1  # increase page offset

        # ===============

        # calcuate IDF
        Tfidf().create_inverse_document_frequency()

        # calcuate PageRank
        # PageRank()