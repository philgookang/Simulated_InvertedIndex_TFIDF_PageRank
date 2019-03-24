from model import *
import collections, math
import time

class Tfidf:

    def __init__(self):
        self.tmp_inverted_index_list = []
        self.tmp_term_frequency_list = []
        self.CREATE_LIMIT           = 30000
        self.RETREIEVE_LIMIT        = 12000

    def check_leftover(self):

        if len(self.tmp_inverted_index_list):
            InvertedIndexM().createmany(self.tmp_inverted_index_list)
            self.tmp_inverted_index_list.clear()

        if len(self.tmp_term_frequency_list):
            TermTFM().createmany(self.tmp_term_frequency_list)
            self.tmp_term_frequency_list.clear()

    def create_inverted_index(self, wiki, tokenized_word):

        # remove duplicates
        tokenized_word_list = set(tokenized_word)

        # insert each work to inverted_index table
        for word in tokenized_word_list:

            self.tmp_inverted_index_list.append( (word, wiki["id"], word) )

            if len(self.tmp_inverted_index_list) % self.CREATE_LIMIT == 0:
                InvertedIndexM().createmany(self.tmp_inverted_index_list)
                self.tmp_inverted_index_list.clear()

    def create_term_frequency(self, wiki, tokenized_word):

        # n(d) save the total number of terms in document
        total_term_count = len(set(tokenized_word))

        # n(d,t) get number if occurences of the term t in document d
        term_counter = collections.Counter(tokenized_word)

        # loop through the keys
        for term in term_counter:

            # number of occurrences
            term_count = term_counter[term]

            # TF(d,t) = log(1 + n(d,t)/n(d))
            tf = math.log(1 + (term_count / total_term_count))

            # add to create list
            self.tmp_term_frequency_list.append((term, wiki["id"], term_count, tf))

            if len(self.tmp_term_frequency_list) % self.CREATE_LIMIT == 0:
                TermTFM().createmany(self.tmp_term_frequency_list)
                self.tmp_term_frequency_list.clear()

    def create_inverse_document_frequency(self):

        limit       = self.RETREIEVE_LIMIT
        offset      = 0
        tmp_list    = []
        # start       = time.time()

        while True:

            term_list = TermTFM().getList(limit=limit, offset=(limit * offset))

            if not len(term_list):break

            for term in term_list:

                idf = (1 / term["cnt"])
                tf_idf = (term["tf"] / idf)

                tmp_list.append( (term["term"], term["id"], idf, tf_idf) )

                if len(tmp_list) % self.CREATE_LIMIT == 0:
                    TermIDFM().createmany(tmp_list)
                    tmp_list.clear()

                # if len(tmp_list)%1000 == 0:
                #     print("middle ", (time.time() - start) )
                #     start = time.time()

            offset = offset + 1

        if len(tmp_list):
            TermIDFM().createmany(tmp_list)