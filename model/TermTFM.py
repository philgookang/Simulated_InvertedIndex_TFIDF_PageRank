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

    def getList2(self, **kwargs):

        sort_by     = kwargs['sort_by']             if 'sort_by'            in kwargs else 'term'
        sdirection  = kwargs['sort_direction']     if 'sort_direction'   in kwargs else 'asc'
        limit       = kwargs['limit']               if 'limit'              in kwargs else 20
        nolimit     = kwargs['nolimit']             if 'nolimit'            in kwargs else False
        offset      = kwargs['offset']              if 'offset'             in kwargs else 0
        group_by    = kwargs['group_by']            if 'group_by'           in kwargs else ''
        count       = kwargs['count']               if 'count'              in kwargs else False
        select      = kwargs['select']              if 'select'             in kwargs else ' term,id,occurrences,tf '

        query = '''
            SELECT  
                `ttf`.`term`, 
                `ttf`.`id`, 
                `ttf`.`occurrences`, 
                `ttf`.`tf`,
                (
                    SELECT 
                        count(term)
                    FROM
                        `inverted_index`
                    WHERE
                        `inverted_index`.`term` COLLATE utf8mb4_bin = `ttf`.`term`
                    GROUP BY
                        `inverted_index`.`term`
                ) as `cnt`
            FROM 
                `term_tf` `ttf`
            ORDER BY 
                {0} {1}
            LIMIT 
                %s 
            OFFSET 
                %s 
        '''.format(sort_by, sdirection)

        return self.postman.getList(query, [ limit, offset ])

    def getList3(self, **kwargs):

        sort_by     = kwargs['sort_by']             if 'sort_by'            in kwargs else 'term'
        sdirection  = kwargs['sort_direction']     if 'sort_direction'   in kwargs else 'asc'
        limit       = kwargs['limit']               if 'limit'              in kwargs else 20
        nolimit     = kwargs['nolimit']             if 'nolimit'            in kwargs else False
        offset      = kwargs['offset']              if 'offset'             in kwargs else 0
        group_by    = kwargs['group_by']            if 'group_by'           in kwargs else ''
        count       = kwargs['count']               if 'count'              in kwargs else False
        select      = kwargs['select']              if 'select'             in kwargs else ' term,id,occurrences,tf '

        query = '''
            SELECT 
                count(`inverted_index`.`term`) as cnt,
                `ttf`.`term`, 
                `ttf`.`id`, 
                `ttf`.`occurrences`, 
                `ttf`.`tf`
            FROM
                `inverted_index`,
                (
                    SELECT  
                        `term`, 
                        `id`, 
                        `occurrences`, 
                        `tf`
                    FROM 
                        `term_tf`
                    ORDER BY 
                        {0} {1}
                    LIMIT 
                        %s 
                    OFFSET 
                        %s
                ) as ttf
            WHERE
                `inverted_index`.`term` COLLATE utf8mb4_bin = `ttf`.`term`
            GROUP BY
                `inverted_index`.`term`,
                `ttf`.`term`, 
                `ttf`.`id`, 
                `ttf`.`occurrences`, 
                `ttf`.`tf`
        '''.format(sort_by, sdirection)

        return self.postman.getList(query, [ limit, offset ])


    def getList(self, **kwargs):

        sort_by     = kwargs['sort_by']             if 'sort_by'            in kwargs else 'term'
        sdirection  = kwargs['sort_direction']     if 'sort_direction'   in kwargs else 'asc'
        limit       = kwargs['limit']               if 'limit'              in kwargs else 20
        nolimit     = kwargs['nolimit']             if 'nolimit'            in kwargs else False
        offset      = kwargs['offset']              if 'offset'             in kwargs else 0
        group_by    = kwargs['group_by']            if 'group_by'           in kwargs else ''
        count       = kwargs['count']               if 'count'              in kwargs else False
        select      = kwargs['select']              if 'select'             in kwargs else ' term,id,occurrences,tf '

        query = "SELECT "
        query += select
        query += " FROM "
        query +=    "`term_tf` "
        query += group_by
        query += "ORDER BY {0} {1} ".format(sort_by, sdirection)
        if not nolimit and not count:         query += "LIMIT %s offset %s "

        params = []
        if not nolimit and not count:         params.extend((limit, offset))

        return self.postman.getList(query, params)