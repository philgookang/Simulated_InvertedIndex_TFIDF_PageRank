from system import *

class InvertedIndexM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def createmany(self, lst):
        query = '''
            INSERT INTO `inverted_index`
                ( `term`, `id`, `term_encod`)
            VALUES
                ( %s, %s, %s )
        '''
        self.postman.executemany(query, lst)