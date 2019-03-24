from model import *
import collections, math

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
            tmp_list.append( (word, self.wiki["id"], index) )
            if index % 300 == 0:
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
            tmp_list.append((term, self.wiki["id"], term_count, tf, 0, 0))

            if index % 300 == 0:
                # create term frequency to database
                TermTFM().createmany(tmp_list)

                # clear list
                tmp_list.clear()

        if len(tmp_list):
            TermTFM().createmany(tmp_list)

    def create_inverse_document_frequency(self):

        limit = 100
        offset = 0

        while True:

            term_list = TermTFM().getList(limit=limit, offset=(limit * offset))

            if not len(term_list):break

            for term in term_list:
                occurrences = InvertedIndexM({"term": term["term"]}).getOccurrences()
                idf     = 0
                tf_idf  = 0
                if 'cnt' in occurrences:
                    idf     = (1 / occurrences["cnt"])
                    tf_idf  = (term["tf"] / idf)
                else:
                    print("cnt error " , term, occurrences)

                # TermM({"id": term["id"], "term": term["term"], "idf": idf, "tf_idf": tf_idf }).update()
                # add to termidf

            offset = offset + 1