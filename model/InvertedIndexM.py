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

    def search(self):
        query = '''
            SELECT 
                `ii`.`term`,
                `ii`.`id`,
                `pr`.`probability`,
                `t`.`tf`,
                `t`.`idf`,
                `t`.`tf_idf`
            FROM 
                `inverted_index` `ii`,
                `page_rank` `pr`,
                `term` `t`
            WHERE 
                    `ii`.`id` = `pr`.id 
                AND
                    `ii`.`id` = `t`.`id`
                AND 
                    `ii`.`term` = `t`.`term`
                AND
                    `ii`.`term` = 'was' 
            GROUP BY 
                `ii`.`term`,
                `ii`.`id`,
                `pr`.`probability`,
                `t`.`tf`,
                `t`.`idf`,
                `t`.`tf_idf`
            ORDER BY
                
        '''