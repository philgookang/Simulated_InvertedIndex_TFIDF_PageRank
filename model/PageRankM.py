from system import *

class PageRankM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def createmany(self, lst):
        query = '''
            INSERT INTO `page_rank`
                ( `id`, `probability`)
            VALUES
                ( %s, %s )
        '''
        return self.postman.executemany(query, lst)

    def get(self):
        query = '''
            SELECT
                `id`
            FROM 
                `page_rank`
            WHERE
                `id` = %s
        '''
        return self.postman.get(query, [self.id])