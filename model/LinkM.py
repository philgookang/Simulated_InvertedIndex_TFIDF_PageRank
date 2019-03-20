from system import *

class LinkM:

    def __init__(self, dicts = {}):
        self.postman = Database.init()
        for key,val in dicts.items():
            setattr(self, str(key), val)

    def getList(self, **kwargs):

        sort_by     = kwargs['sort_by']             if 'sort_by'            in kwargs else 'id_to'
        sdirection  = kwargs['sort_direction']     if 'sort_direction'   in kwargs else 'asc'
        limit       = kwargs['limit']               if 'limit'              in kwargs else 20
        nolimit     = kwargs['nolimit']             if 'nolimit'            in kwargs else False
        offset      = kwargs['offset']              if 'offset'             in kwargs else 0
        group_by    = kwargs['group_by']            if 'group_by'           in kwargs else ''
        count       = kwargs['count']               if 'count'              in kwargs else False
        select      = kwargs['select']              if 'select'             in kwargs else ' id_from,id_to '

        query = "SELECT "
        query += select
        query += " FROM "
        query +=    "`link` "
        query += " WHERE "
        query += "`id_from` = %s "
        query += group_by
        query += "ORDER BY {0} {1} ".format(sort_by, sdirection)
        if not nolimit and not count:         query += "LIMIT %s offset %s "

        params = [self.id_from]
        if not nolimit and not count:         params.extend((limit, offset))

        return self.postman.getList(query, params)