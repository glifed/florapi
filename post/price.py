import postgresql

import basic as basic
import global_params as gp


def add_price():
    (json, errors) = basic.price_validate()

    if errors:
        return basic.resp(400, {"errors": errors})

    prices = json['prices']
    i = 0
    for item in prices:
        if (not 'code' in item) or \
           (not 'name' in item) or \
           (not 'parentcode' in item) or \
           (not 'price' in item):

            return basic.resp(400, {"errors": "Haven't value"})
        else:
            try:
                with postgresql.open(gp.dbconnect) as db:
                    id_item = db.query("SELECT itemid FROM root.item WHERE importcode = '" + str(item['code']) + "'")

                    if id_item == []:
                        id_item = db.query(str("INSERT INTO root.item(name, longname, avaliable, position, importcode, itemgroupid) "
                                               "VALUES('{0}', '{0}', 1, 999, '{1}', "
                                                    "(SELECT itemgroupid FROM root.itemgroup WHERE importcode = '{2}')"
                                                      ") RETURNING itemid"
                                               ).format(str(item['name']), str(item['code']), str(item['parentcode'])))
                    else:
                        itemgroupid = db.query(str("SELECT itemgroupid FROM root.itemgroup WHERE importcode = '" + str(item['parentcode']) + "'"))
                        if len(itemgroupid) == 1:
                            db.query(str("UPDATE root.item SET itemgroupid = "
                                         "(SELECT itemgroupid FROM root.itemgroup WHERE importcode = '" + str(item['parentcode']) + "') "
                                         "WHERE itemid = " + str(id_item[0][0])))
                        else:
                            db.query(str("UPDATE root.item SET itemgroupid = 0 "                                         
                                         "WHERE itemid = " + str(id_item[0][0])))

                    id_global = db.query(str("SELECT globalitemsid FROM root.globalitems "
                                             "WHERE status = 1 AND itemid = " + str(id_item[0][0])))

                    id_price = db.query(str("SELECT priceid FROM root.price "
                                             "WHERE pricelistid = 1 "
                                                   "AND itemid = " + str(id_item[0][0]) + " "
                                                   "AND globalid = " + str(id_global[0][0])))

                    if id_price == []:
                        db.query(str("INSERT INTO root.price(itemid, globalid, price, pricelistid) "
                                     "VALUES({0}, {1}, {2}, 1)"
                                     ).format(str(id_item[0][0]), str(id_global[0][0]), str(item['price'])))
                    else:
                        db.query(str("UPDATE root.price SET price = " + str(item['price']) + " "
                                     "WHERE priceid = " + str(id_price[0][0])))
            except:
                return basic.resp(400, {"errors": "Haven't connect with base"})

    return basic.resp(200, {})
