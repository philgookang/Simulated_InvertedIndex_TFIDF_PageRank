from system import *

class Setup:

    def __init__(self):
        self.postman = Database.init()

        self.drop_tables()
        self.create_tables()
        self.add_indexes()

    def drop_tables(self):
        self.postman.execute(" DROP TABLE IF EXISTS `ADB2018_22788`.`inverted_index` ")
        self.postman.execute(" DROP TABLE IF EXISTS `ADB2018_22788`.`page_rank` ")
        self.postman.execute(" DROP TABLE IF EXISTS `ADB2018_22788`.`term_tf` ")
        self.postman.execute(" DROP TABLE IF EXISTS `ADB2018_22788`.`term_idf` ")

    def create_tables(self):
        query_inverted_index = '''
            CREATE TABLE `inverted_index` (
              `term` varchar(700) NOT NULL COMMENT '개별단어',
              `id` int(11) NOT NULL COMMENT '해당 단어가 포함된 문서 id',
              `term_encod` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        query_page_rank = '''
            CREATE TABLE `page_rank` (
              `id` int(11) NOT NULL,
              `probability` double NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        query_term_tf = '''
            CREATE TABLE `term_tf` (
              `term` varchar(700) NOT NULL,
              `id` int(11) NOT NULL,
              `occurrences` int(11) NOT NULL,
              `tf` double NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        query_term_idf = '''
            CREATE TABLE `term_idf` (
              `term` varchar(700) NOT NULL,
              `id` int(11) NOT NULL,
              `idf` double NOT NULL,
              `tf_idf` double NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        self.postman.execute(query_inverted_index)
        self.postman.execute(query_page_rank)
        self.postman.execute(query_term_tf)
        self.postman.execute(query_term_idf)

    def add_indexes(self):
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `term`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `id`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `term`, `id`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `term_encod`); ")
        self.postman.execute(" ALTER TABLE `inverted_index` ADD INDEX( `id`, `term_encod`); ")

        self.postman.execute(" ALTER TABLE `page_rank` ADD INDEX( `id`); ")
        self.postman.execute(" ALTER TABLE `page_rank` ADD INDEX( `probability`); ")
        self.postman.execute(" ALTER TABLE `page_rank` ADD INDEX( `id`, `probability`); ")

        self.postman.execute(" ALTER TABLE `term_tf` ADD INDEX( `term`); ")
        self.postman.execute(" ALTER TABLE `term_tf` ADD INDEX( `id`); ")
        self.postman.execute(" ALTER TABLE `term_tf` ADD INDEX( `tf`); ")

        self.postman.execute(" ALTER TABLE `term_tf` ADD INDEX( `term`, `id`); ")
        self.postman.execute(" ALTER TABLE `term_tf` ADD INDEX( `term`, `tf`); ")
        self.postman.execute(" ALTER TABLE `term_tf` ADD INDEX( `id`, `tf`); ")

        self.postman.execute(" ALTER TABLE `term_idf` ADD INDEX( `term`); ")
        self.postman.execute(" ALTER TABLE `term_idf` ADD INDEX( `id`); ")
        self.postman.execute(" ALTER TABLE `term_idf` ADD INDEX( `term`, `id`); ")
        self.postman.execute(" ALTER TABLE `term_idf` ADD INDEX( `idf`); ")
        self.postman.execute(" ALTER TABLE `term_idf` ADD INDEX( `tf_idf`); ")
        self.postman.execute(" ALTER TABLE `term_idf` ADD INDEX( `term`, `id`, `idf`); ")
        self.postman.execute(" ALTER TABLE `term_idf` ADD INDEX( `term`, `id`, `tf_idf`); ")

