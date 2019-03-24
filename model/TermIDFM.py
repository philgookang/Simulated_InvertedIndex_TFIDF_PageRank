from system import *

class TermIDFM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def createmany(self, lst):
        query = '''
            INSERT INTO `term_idf`
                ( `term`, `id`, `idf`, `tf_idf`)
            VALUES
                ( %s, %s, %s, %s )
        '''
        return self.postman.executemany(query, lst)