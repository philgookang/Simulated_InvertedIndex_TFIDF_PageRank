from model import *
import collections

class PageRank:

    def __init__(self):
        self.page_probabilities = {} # holds the latest probability for each page
        self.getWikies()
        self.calculate()

    def getWikies(self):

        offset          = 0  # pagination offset
        limit           = 1000 # number of items to load per page
        self.wiki_list  = [] # holds all the wiki pages

        while True:  # keep running until we have completed loaded

            # get list of wiki
            tmp_list = LinkM().getList(limit=limit, offset=(limit * offset), select=' DISTINCT id_from as id ', sort_by = ' id_from ')

            # check if list is empty
            if not len(tmp_list):
                break

            # add content
            self.wiki_list.extend(tmp_list)

            # increase offset
            offset = offset + 1

    def calculate(self, attempt = 0):

        N               = len(self.wiki_list)       # total number of pages
        epsilon         = 0.15                      # jump to any other node with probability E
        total_change    = 0                         # total change in probability

        # loop through wiki list
        for current_id,current_wiki in enumerate(self.wiki_list):

            summation_probability = 0.0

            linked_wiki_list = LinkM({ "id_to" : current_wiki['id'] }).getList(nolimit = True, select = " id_from ")

            for other_id,other_wiki in enumerate(linked_wiki_list):

                # get leaving list
                link_list   = LinkM({ "id_from" : other_wiki["id_from"] }).getList(nolimit = True, select = " id_to ")
                link_count  = len(link_list)

                # if has no links skip!
                if not link_count: continue

                # convert list-dictionary to list
                link_target_list    = list(map(lambda x : x["id_to"], link_list))
                link_target_counter = collections.Counter(link_target_list)

                # calculate current probabilities
                if attempt != 0 and other_wiki["id_from"] in self.page_probabilities:
                    probability = self.page_probabilities[ other_wiki["id_from"] ]
                else:
                    probability = (1 / N)

                # number of links going to currrent wiki / total number of links
                link_probability = link_target_counter[current_wiki['id']] / link_count

                # add up all the summation values
                summation_probability = summation_probability + (probability * link_probability)

            # get page rank probability
            page_rank_probability = (epsilon/N) + (1 - epsilon) * summation_probability

            if attempt != 0:
                # save the total change
                total_change = total_change + abs(self.page_probabilities[ current_wiki['id'] ] - page_rank_probability)

            # keep page rank local version
            self.page_probabilities[ current_wiki['id'] ] = page_rank_probability

        if attempt == 0  or total_change > 0.000000001:
            print("total change", total_change, attempt)
            self.calculate( (attempt + 1) )
        else:
            # save to database the new probability
            self.saveProbability()

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


