from model import *
import collections, math
import time

class Tfidf:

    def __init__(self, wiki = [], tokenized_word = []):
        self.wiki = wiki
        self.tokenized_word = tokenized_word

    def create_inverted_index(self):

        # remove duplicates
        tokenized_word_list = set(self.tokenized_word)

        # holds lst to insert
        tmp_list = []

        # insert each work to inverted_index table
        for index, word in enumerate(tokenized_word_list):

            tmp_list.append( (word, self.wiki["id"]) )

            if len(tmp_list) % 7000 == 0:
                InvertedIndexM().createmany(tmp_list)
                tmp_list.clear()

        # check for any left overs!
        if len(tmp_list):
            InvertedIndexM().createmany(tmp_list)

    def create_term_frequency(self):

        # n(d) save the total number of terms in document
        total_term_count = len(set(self.tokenized_word))

        # n(d,t) get number if occurences of the term t in document d
        term_counter = collections.Counter(self.tokenized_word)

        # tmp list to hold insert
        tmp_list = []

        # loop through the keys
        for index,term in enumerate(term_counter):

            # number of occurrences
            term_count = term_counter[term]

            # TF(d,t) = log(1 + n(d,t)/n(d))
            tf = math.log(1 + (term_count / total_term_count))

            # add to create list
            tmp_list.append((term, self.wiki["id"], term_count, tf))

            if len(tmp_list) % 7000 == 0:
                TermTFM().createmany(tmp_list)
                tmp_list.clear()

        if len(tmp_list):
            TermTFM().createmany(tmp_list)

    def create_inverse_document_frequency(self):

        start = time.time()

        limit       = 500
        offset      = 0
        tmp_list    = []

        while True:

            term_list = TermTFM().getList3(limit=limit, offset=(limit * offset))

            if not len(term_list):break

            for index, term in enumerate(term_list):

                idf = (1 / term["cnt"])
                tf_idf = (term["tf"] / idf)

                tmp_list.append( (term["term"], term["id"], idf, tf_idf) )

                if len(tmp_list) % 7000 == 0:
                    TermIDFM().createmany(tmp_list)
                    tmp_list.clear()

            if len(tmp_list) == 1000:
                print(time.time()-start)

            offset = offset + 1

        if len(tmp_list):
            TermIDFM().createmany(tmp_list)

        #
        # limit       = 100
        # offset      = 0
        # tmp_list    = []
        #
        # while True:
        #
        #     term_list = TermTFM().getList(limit=limit, offset=(limit * offset))
        #
        #     if not len(term_list):break
        #
        #     for index, term in enumerate(term_list):
        #         occurrences = InvertedIndexM({"term": term["term"]}).getOccurrences()
        #         idf     = 0
        #         tf_idf  = 0
        #         if 'cnt' in occurrences:
        #             idf     = (1 / occurrences["cnt"])
        #             tf_idf  = (term["tf"] / idf)
        #         else:
        #             print("cnt error " , term, occurrences)
        #
        #         tmp_list.append( (term["term"], term["id"], idf, tf_idf) )
        #
        #         if len(tmp_list) % 7000 == 0:
        #             TermIDFM().createmany(tmp_list)
        #             tmp_list.clear()
        #
        #
        #     if len(tmp_list) == 1000:
        #         print(time.time()-start)
        #
        #     offset = offset + 1
        #
        # if len(tmp_list):
        #     TermIDFM().createmany(tmp_list)