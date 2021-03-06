from system import *

class WikiM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def getList(self, **kwargs):

        sort_by     = kwargs['sort_by']             if 'sort_by'            in kwargs else 'id'
        sdirection  = kwargs['sort_direction']     if 'sort_direction'   in kwargs else 'desc'
        limit       = kwargs['limit']               if 'limit'              in kwargs else 20
        nolimit     = kwargs['nolimit']             if 'nolimit'            in kwargs else False
        offset      = kwargs['offset']              if 'offset'             in kwargs else 0
        count       = kwargs['count']               if 'count'              in kwargs else False
        select      = kwargs['select']              if 'select'             in kwargs else ' id,title,text '

        query = "SELECT "
        query += select
        query += " FROM "
        query +=    "`wiki` "
        query += "ORDER BY {0} {1} ".format(sort_by, sdirection)
        if not nolimit and not count:         query += "LIMIT %s offset %s "

        params = []
        if not nolimit and not count:         params.extend((limit, offset))

        return self.postman.getList(query, params)