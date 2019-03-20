from model import *
import nltk
import re
import nltk.tokenize.punkt as aaa

class Initalize:

    def __init__(self):
        self.create_inverted_index()

    def create_inverted_index(self):

        # pagination offset
        offset = 0

        # number of items to load per page
        limit = 10

        # create inverted index for each wiki
        while True:

            # get list of wiki
            wiki_list = WikiM().getList(limit=limit, offset=(limit*offset))

            # loop through wiki list
            for wiki in wiki_list:

                tok_cls = aaa.PunktSentenceTokenizer
                train_cls = aaa.PunktTrainer

                # tokensize by sentence
                # tokenized_sentence = nltk.sent_tokenize(wiki["text"])

                cleanup = (
                    lambda s: re.compile(r'(?:\r|^\s+)', re.MULTILINE).sub('', s).replace('\n', ' ')
                )
                trainer = train_cls()
                trainer.INCLUDE_ALL_COLLOCS = True
                trainer.train(wiki["text"])
                sbd = tok_cls(trainer.get_params())
                for l in sbd.sentences_from_text(wiki["text"]):
                    # print(cleanup(l))

                    # get tokenized word
                    tokenized_word = nltk.word_tokenize(l)

                    # insert each work to inverted_index table
                    for index, word in enumerate(tokenized_word):
                        inverted_index = InvertedIndexM({ "id" : wiki["id"], "term" : word, "location" : index })
                        inverted_index.create()
                break

            # increase page offset
            offset = offset + 1

