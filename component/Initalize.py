from model import *
import nltk
import collections
import math

class Initalize:

    def __init__(self):

        offset = 0 # pagination offset
        limit = 10 # number of items to load per page

        while True: # create inverted index for each wiki

            # get list of wiki
            wiki_list = WikiM().getList(limit=limit, offset=(limit * offset))

            # check if list is empty
            if not len(wiki_list): break

            # loop through wiki list
            for wiki in wiki_list:
                # get tokenized word
                tokenized_word = nltk.wordpunct_tokenize(wiki["text"])

                # create inverted index
                self.create_inverted_index(wiki, tokenized_word)

                # calcuate tf, idf, tfidf
                self.create_term_frequency(wiki, tokenized_word)
                break
            break

            offset = offset + 1  # increase page offset

        # ===============

        self.create_inverse_document_frequency()

    def create_inverted_index(self, wiki, tokenized_word):

        # insert each work to inverted_index table
        for index, word in enumerate(tokenized_word):
            inverted_index = InvertedIndexM({"id": wiki["id"], "term": word, "location": index})
            inverted_index.create()

    def create_term_frequency(self, wiki, tokenized_word):

        # n(d) save the total number of terms in document
        total_term_count = len(tokenized_word)

        # n(d,t) get number if occurences of the term t in document d
        term_counter = collections.Counter(tokenized_word)

        # loop through the keys
        for term in term_counter:

            # number of occurrences
            term_count = term_counter[term]

            # TF(d,t) = log(1 + n(d,t)/n(d))
            tf = math.log( 1 +  (term_count / total_term_count))

            # create term frequency to database
            TermM({ "id" : wiki["id"], "term" : term, "occurrences" : term_count, "tf" : tf })


    def create_inverse_document_frequency(self):

        limit = 10
        offset = 0

        while True:

            term_list = TermM().getList( limit = limit, offset=(limit * offset))

            for term in term_list:
                occurrences = InvertedIndexM({"term":term["term"]}).getOccurrences()
                idf = (1 / occurrences["cnt"])
                tf_idf = (term["tf"] / idf)



#            inverted_index_list = InvertedIndexM().getList( select = " count(id) as occurrence,term ", group_by=" GROUP BY name ", limit=limit, offset=(limit*offset))

 #           for inverted_index in inverted_index_list:

  #              idf = (1 / inverted_index["occurrence"])

