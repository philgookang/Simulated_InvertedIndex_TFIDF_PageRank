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

    def getOccurrences(self):

        query = '''
            SELECT 
                count(term) as cnt
            FROM
                `inverted_index`
            WHERE
                `term` COLLATE utf8mb4_bin = %s
            GROUP BY
                `term`
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