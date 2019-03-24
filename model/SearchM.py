from system import *

class SearchM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def search(self, search_list):

        search_query = ""

        for index,word in enumerate(search_list):
            if index != 0:
                search_query = search_query + " , "
            search_query = search_query + " %s "


        query = '''
            SELECT 
                `wiki`.`title`,
                `wiki`.`id`,
                `tidf`.`sim_tf_idf` as `idf`,
                `page_rank`.`probability` as `page_rank_score`,
                ( `tidf`.`sim_tf_idf` * `page_rank`.`probability` ) total_value
            FROM
                (
                    SELECT
                        `tidf`.`id`,
                        SUM(`tidf`.tf_idf) as sim_tf_idf
                    FROM
                        `term_idf` `tidf`
                    WHERE
                        `tidf`.`term` IN ( {0} )
                    GROUP BY
                        `tidf`.`id`
                ) as tidf,
                `page_rank`,
                `wiki`
            WHERE
                    `tidf`.`id` = `page_rank`.`id` 
                AND
                    `tidf`.`id` = `wiki`.`id`
            ORDER BY
                ( `tidf`.`sim_tf_idf` * `page_rank`.`probability` ) DESC,
                `wiki`.`id` ASC
            LIMIT
                %s
            OFFSET 
                %s
        '''.format(search_query)

        params = []
        params.extend(search_list)
        params.extend([10, 0])

        return self.postman.getList(query, params)