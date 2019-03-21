from model import *
import collections, math

class Tfidf:

    def __init__(self, wiki = [], tokenized_word = []):
        self.wiki = wiki
        self.tokenized_word = tokenized_word

    def create_inverted_index(self):

        # insert each work to inverted_index table
        for index, word in enumerate(self.tokenized_word):
            inverted_index = InvertedIndexM({"id": self.wiki["id"], "term": word, "location": index})
            inverted_index.create()

    def create_term_frequency(self):

        # n(d) save the total number of terms in document
        total_term_count = len(set(self.tokenized_word))

        # n(d,t) get number if occurences of the term t in document d
        term_counter = collections.Counter(self.tokenized_word)

        # loop through the keys
        for term in term_counter:

            # number of occurrences
            term_count = term_counter[term]

            # TF(d,t) = log(1 + n(d,t)/n(d))
            tf = math.log(1 + (term_count / total_term_count))

            # create term frequency to database
            TermM({"id": self.wiki["id"], "term": term, "occurrences": term_count, "tf": tf}).create()

    def create_inverse_document_frequency(self):

        limit = 100
        offset = 0

        while True:

            term_list = TermM().getList(limit=limit, offset=(limit * offset))

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

                TermM({"id": term["id"], "term": term["term"], "idf": idf, "tf_idf": tf_idf }).update()

            offset = offset + 1