import postgresql

import basic as basic
import global_params as gp


def add_store():
    (json, errors) = basic.store_validate()

    if errors:
        return basic.resp(400, {"errors": errors})

    stores = json['stores']
    for item in stores:
        if (not 'code' in item) or \
           (not 'name' in item) or \
           (not 'store' in item) or \
           (not 'parentcode' in item):
            return basic.resp(400, {"errors": "Haven't value"})
        else:
            try:
                with postgresql.open(gp.dbconnect) as db:
                    id_item = db.query("SELECT itemid FROM root.item WHERE importcode = '" + str(item['code']) + "'")
                    itemgroupid = db.query(str("SELECT itemgroupid "
                                               "FROM root.itemgroup "
                                               "WHERE importcode = '" + str(item['parentcode']) + "'"))

                    if id_item == []:
                        id_item = db.query(str("INSERT INTO root.item(name, avaliable, position, importcode) "
                                               "VALUES('{0}', 1, 999, '{1}') RETURNING itemid"
                                               ).format(str(item['name']), str(item['code'])))
                    else:
                        if len(itemgroupid[0]) == 1:
                            db.query(str("UPDATE root.item SET itemgroupid = " + str(itemgroupid[0][0]) + " "
                                         "WHERE itemid = " + str(id_item[0][0])))
                        else:
                            db.query(str("UPDATE root.item SET itemgroupid = 0 "
                                         "WHERE itemid = " + str(id_item[0][0])))
                    id_global = db.query(str("SELECT globalitemsid FROM root.globalitems "
                                             "WHERE status = 1 AND itemid = " + str(id_item[0][0])))

                    id_store = db.query(str("SELECT storeid FROM root.store "
                                            "WHERE stationid = 1 "
                                                  "AND itemid = " + str(id_item[0][0]) + " "
                                                  "AND globalid = " + str(id_global[0][0])))

                    if id_store == []:
                        db.query(str("INSERT INTO root.store(itemid, globalid, value, stationid) "
                                     "VALUES({0}, {1}, {2}, 1)"
                                     ).format(str(id_item[0][0]), str(id_global[0][0]), str(item['store'])))
                    else:
                        db.query(str("UPDATE root.store SET value = " + str(item['store']) + " "
                                     "WHERE storeid = " + str(id_store[0][0])))
            except:
                return basic.resp(400, {"errors": "Haven't connect with base"})

    return basic.resp(200, {})
