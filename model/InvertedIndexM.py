from system import *

class InvertedIndexM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def create(self):
        query = '''
            INSERT INTO `inverted_index`
                ( `term`, `id`, `location`)
            VALUES
                ( %s, %s, %s )
        '''
        return self.postman.create(query, [self.term, self.id, self.location])

    def getOccurrences(self):

        query = '''
            SELECT 
                count(id) as cnt
            FROM
                `inverted_index`
            WHERE
                `term`=%s
            GROUP BY
                `id`
        '''
        return self.postman.get(query, [self.term])