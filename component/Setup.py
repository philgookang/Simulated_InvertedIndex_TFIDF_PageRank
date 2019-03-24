from system import *

class Setup:

    def __init__(self):
        self.postman = Database.init()

        self.drop_tables()
        self.create_tables()
        self.add_indexes()

    def drop_tables(self):
        self.postman.execute(" DROP TABLE `inverted_index` ")
        self.postman.execute(" DROP TABLE `page_rank` ")
        self.postman.execute(" DROP TABLE `term` ")

    def create_tables(self):
        query_inverted_index = '''
            CREATE TABLE `inverted_index` (
              `term` varchar(700) NOT NULL COMMENT '개별단어',
              `id` int(11) NOT NULL COMMENT '해당 단어가 포함된 문서 id',
              `location` int(11) NOT NULL COMMENT '문구에 순서 위치'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        query_page_rank = '''
            CREATE TABLE `page_rank` (
              `id` int(11) NOT NULL,
              `probability` double NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        query_term = '''
            CREATE TABLE `term_tf` (
              `term` varchar(700) NOT NULL,
              `id` int(11) NOT NULL,
              `occurrences` int(11) NOT NULL,
              `tf` double NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        query_term = '''
            CREATE TABLE `term_idf` (
              `term` varchar(700) NOT NULL,
              `id` int(11) NOT NULL,
              `idf` double NOT NULL,
              `tf_idf` double NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        self.postman.execute(query_inverted_index)
        self.postman.execute(query_page_rank)
        self.postman.execute(query_term)

    def add_indexes(self):
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `term`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `id`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `location`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `id`, `location`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `term`, `id`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `term`, `location`); ")

        self.postman.execute(" ALTER TABLE `page_rank` ADD INDEX( `id`); ")
        self.postman.execute(" ALTER TABLE `page_rank` ADD INDEX( `probability`); ")
        self.postman.execute(" ALTER TABLE `page_rank` ADD INDEX( `id`, `probability`); ")

        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `term`); ")
        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `id`); ")
        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `term`, `id`); ")
        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `tf`); ")
        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `idf`); ")
        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `tf_idf`); ")
        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `idf`, `tf_idf`); ")
        self.postman.execute(" ALTER TABLE `term` ADD INDEX( `tf`, `idf`); ")

