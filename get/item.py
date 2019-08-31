import postgresql

import basic as basic
import global_params as gp


def items():
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT i.itemid, i.name "
                          "FROM root.item i "
                          "WHERE i.avaliable = 1")
        items = []
        for (itemid, name) in tuples:
            items.append({ "id": itemid, "name": name })
        return basic.resp(200, {"items": items})


def item(item_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT i.itemid, i.name "
                          "FROM root.item i "
                          "WHERE i.avaliable = 1 AND itemid = " + str(item_id))
        items = []
        for (itemid, name) in tuples:
            items.append({ "id": itemid, "name": name })
        return basic.resp(200, {"items": items})


def items_group(group_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT i.itemid, i.name "
                          "FROM root.item i "
                          "WHERE i.avaliable = 1 AND itemgroupid = " + str(group_id))
        items = []
        for (itemid, name) in tuples:
            items.append({ "id": itemid, "name": name })
        return basic.resp(200, {"items": items})

