import postgresql

import basic as basic
import global_params as gp


def prices():
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT p.itemid, p.price, p.pricelistid "
                          "FROM root.price p "
                          "INNER JOIN root.item i ON i.itemid = p.itemid "
                          "WHERE i.avaliable = 1 AND p.price > 0.0")
        prices = []
        for (itemid, price, pricelistid) in tuples:
            prices.append({"id": itemid, "price": float(price), "pricelist": int(pricelistid)})
        return basic.resp(200, {"prices": prices})


def prices_pricelist(pricelist_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT p.itemid, p.price, p.pricelistid "
                          "FROM root.price p "
                          "INNER JOIN root.item i ON i.itemid = p.itemid "
                          "WHERE p.pricelistid = " + str(pricelist_id) + " AND i.avaliable = 1 AND p.price > 0.0")
        prices = []
        for (itemid, price, pricelistid) in tuples:
            prices.append({ "id": itemid, "price": float(price), "pricelist": int(pricelistid) })
        return basic.resp(200, {"prices": prices})


def price(pricelist_id, item_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT p.itemid, p.price, p.pricelistid "
                          "FROM root.price p "
                          "INNER JOIN root.item i ON i.itemid = p.itemid "
                          "WHERE p.pricelistid = " + str(pricelist_id) + " AND i.avaliable = 1 AND p.price > 0.0 AND i.itemid = " + str(item_id))
        prices = []
        for (itemid, price, pricelistid) in tuples:
            prices.append({ "id": itemid, "price": float(price), "pricelist": int(pricelistid) })
        return basic.resp(200, {"prices": prices})