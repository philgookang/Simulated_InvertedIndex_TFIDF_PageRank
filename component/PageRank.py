from model import *
import collections

class PageRank:

    def __init__(self):
        self.page_probabilities = {} # holds the latest probability for each page
        self.calculate()

    def getWikies(self):

        offset      = 0  # pagination offset
        limit       = 100 # number of items to load per page
        wiki_list   = [] # holds all the wiki pages

        while True:  # keep running until we have completed loaded

            # get list of wiki
            tmp_list = WikiM().getList(limit=limit, offset=(limit * offset), select=' id ')

            # check if list is empty
            if not len(tmp_list):
                break

            # add content
            wiki_list.extend(tmp_list)

            # increase offset
            offset = offset + 1

        return wiki_list

    def checkAllConverge(self):
        for id in self.page_probabilities:
            if self.page_probabilities[id] > 0.000000001:
                return False
        return True

    def calculate(self, attempt = 0):

        wiki_list   =  self.getWikies()         # get list of all wiki pages
        N           = len(wiki_list)            # total number of pages
        epsilon     = 0.15                      # jump to any other node with probability E

        # loop through wiki list
        for current_id,current_wiki in enumerate(wiki_list):

            # check if convergence is below mark
            if current_wiki['id'] in self.page_probabilities and self.page_probabilities[ current_wiki['id'] ] <= 0.000000001:
                continue

            summation_probability = 0.0

            for other_id,other_wiki in enumerate(wiki_list):

                # get leaving list
                link_list   = LinkM({ "id_from" : other_wiki["id"] }).getList(nolimit = True, select = " id_to ")
                link_count  = len(link_list)

                # if has no links skip!
                if not link_count: continue

                # convert list-dictionary to list
                link_target_list    = list(map(lambda x : x["id_to"], link_list))
                link_target_counter = collections.Counter(link_target_list)

                # calculate current probabilities
                if other_wiki["id"] in self.page_probabilities:
                    probability = self.page_probabilities[ other_wiki["id"] ]
                else:
                    probability = (1 / N)


                # number of links going to currrent wiki / total number of links
                link_probability = link_target_counter[current_wiki['id']] / link_count

                # add up all the summation values
                summation_probability = summation_probability + (probability * link_probability)

            # get page rank probability
            page_rank_probability = (epsilon/N) + (1 - epsilon) * summation_probability

            # keep page rank local version
            self.page_probabilities[ current_wiki['id'] ] = page_rank_probability

        # save to database the new probability
        self.saveProbability()

        if not self.checkAllConverge():
            self.calculate( (attempt + 1) )


    def saveProbability(self):

        for id in self.page_probabilities:

            page_rank               = PageRankM()
            page_rank.id            = id
            page_rank.probability   = self.page_probabilities[id]

            check = page_rank.get()

            if 'id' in check:
                page_rank.update()
            else:
                page_rank.create()


