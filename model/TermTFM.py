from system import *

class TermTFM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def createmany(self, lst):
        query = '''
            INSERT INTO `term_tf`
                ( `term`, `id`, `occurrences`, `tf`)
            VALUES
                ( %s, %s, %s, %s)
        '''
        return self.postman.executemany(query, lst)

    def getList(self, **kwargs):

        sort_by     = kwargs['sort_by']             if 'sort_by'            in kwargs else 'term'
        sdirection  = kwargs['sort_direction']     if 'sort_direction'   in kwargs else 'asc'
        limit       = kwargs['limit']               if 'limit'              in kwargs else 20
        offset      = kwargs['offset']              if 'offset'             in kwargs else 0

        query = '''
            SELECT 
                count(`inverted_index`.`term_encod`) as cnt,
                `inverted_index`.`term_encod` as term,
                `ttf`.`id`, 
                `ttf`.`tf`
            FROM
                `inverted_index`,
                (
                    SELECT  
                        `term`, `id`, `tf`
                    FROM 
                        `term_tf`
                    ORDER BY  {0} {1}
                    LIMIT %s 
                    OFFSET %s
                ) as ttf
            WHERE
                `inverted_index`.`term_encod` = `ttf`.`term`
            GROUP BY
                `inverted_index`.`term_encod`,
                `ttf`.`id`, 
                `ttf`.`tf`
        '''.format(sort_by, sdirection)

        return self.postman.getList(query, [ limit, offset ])