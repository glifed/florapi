import postgresql

import basic as basic
import global_params as gp


def groups():
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT g.itemgroupid, g.name, g.parentid, g.color "
                          "FROM root.itemgroup g "
                          "WHERE g.avaliable = 1 "
                          "ORDER BY g.parentid")
        items = []
        for (itemid, name, parentid, color) in tuples:
            items.append({ "id": itemid, "name": name, "parent": parentid, "color": color })
        return basic.resp(200, {"items": items})