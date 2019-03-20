from system import *

class PageRankM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def create(self):
        query = '''
            INSERT INTO `page_rank`
                ( `id`, `probability`)
            VALUES
                ( %s, %s )
        '''
        return self.postman.create(query, [self.id, self.probability])

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

    def update(self):

        query = '''
            UPDATE
                `page_rank`
            SET
                `probability`=%s
            WHERE
                `id`=%s
        '''
        self.postman.execute(query, [ self.probability, self.idf ])