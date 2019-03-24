from model import *
from component.PageRank import PageRank
from component.Tfidf import Tfidf
import nltk, time

class Initalize:

    def __init__(self):

        print("building tables...")

        offset  = 0 # pagination offset
        limit   = 500 # number of items to load per page
        tfidf = Tfidf()

        start = time.time()

        while True: # create inverted index for each wiki

            # get list of wiki
            wiki_list = WikiM().getList(limit=limit, offset=(limit * offset))

            # check if list is empty
            if not len(wiki_list): break

            # loop through wiki list
            for wiki in wiki_list:

                # get tokenized word
                tokenized_word = nltk.tokenize.word_tokenize(wiki["text"])

                # create inverted index
                tfidf.create_inverted_index(wiki, tokenized_word)

                # calcuate tf, idf, tfidf
                tfidf.create_term_frequency(wiki, tokenized_word)

            offset = offset + 1  # increase page offset
        tfidf.check_leftover()

        # ===============

        print("a", (time.time()-start))
        start2 = time.time()

        # calcuate IDF
        Tfidf().create_inverse_document_frequency()

        print("b", (time.time() - start2))

        # calcuate PageRank
        # PageRank()