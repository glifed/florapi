import postgresql

import basic as basic
import global_params as gp

def stores():
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT s.itemid, s.value, s.stationid "
                          "FROM root.store s "
                          "INNER JOIN root.item i ON i.itemid = s.itemid "
                          "WHERE i.avaliable = 1 AND s.value > 0.0")
        stores = []
        for (itemid, store, stationid) in tuples:
            stores.append({ "id": itemid, "store": float(store), "station": int(stationid) })
        return basic.resp(200, {"stores": stores})


def store(station_id, item_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT s.itemid, s.value, s.stationid "
                          "FROM root.store s "
                          "INNER JOIN root.item i ON i.itemid = s.itemid "
                          "WHERE s.stationid = " + str(station_id) + " AND i.avaliable = 1 AND s.value > 0.0 AND i.itemid = " + str(item_id))
        stores = []
        for (itemid, store, stationid) in tuples:
            stores.append({ "id": itemid, "store": float(store), "station": int(stationid) })
        return basic.resp(200, {"stores": stores})


def stores_stantion(station_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT s.itemid, s.value, s.stationid "
                          "FROM root.store s "
                          "INNER JOIN root.item i ON i.itemid = s.itemid "
                          "WHERE s.stationid = " + str(station_id) + " AND i.avaliable = 1 AND s.value > 0.0")
        stores = []
        for (itemid, store, stationid) in tuples:
            stores.append({ "id": itemid, "store": float(store), "station": int(stationid) })
        return basic.resp(200, {"stores": stores})