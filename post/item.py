import postgresql

import basic as basic
import global_params as gp


def add_items():
    (json, errors) = basic.group_validate()

    if errors:
        return basic.resp(400, {"errors": errors})

    groups = json['groups']

    for item in groups:
        if (not 'code' in item) or \
           (not 'name' in item) or \
           (not 'parentcode' in item):
            return basic.resp(400, {"errors": "Haven't value"})
        else:
            try:
                with postgresql.open(gp.dbconnect) as db:
                    id_item = db.query("SELECT itemgroupid FROM root.itemgroup "
                                       "WHERE importcode = '" + str(item['code']) + "'")
                    if id_item == []:
                        db.query(str("INSERT INTO root.itemgroup(name, avaliable, isbig, parentid, importcode) "
                                     "VALUES('{0}', 1, 0, 0, '{1}') RETURNING itemgroupid"
                                    ).format(str(item['name']), str(item['code'])))
            except:
                return basic.resp(400, {"errors": "Haven't connect with base"})

    for item in groups:
        try:
            with postgresql.open(gp.dbconnect) as db:

                if str(item['parentcode']).replace(" ", "") != "":
                    id_itemparent = db.query("SELECT itemgroupid FROM root.itemgroup "
                                             "WHERE importcode = '" + str(item['parentcode']) + "'")

                    db.query(str("UPDATE root.itemgroup SET parentid = " + str(id_itemparent[0][0]) + " "
                                 "WHERE importcode = '" + str(item['code']) + "'"))
        except:
            return basic.resp(400, {"errors": "Haven't connect with base"})

    return basic.resp(200, {})

