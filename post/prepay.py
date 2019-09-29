import datetime

import basic as basic
import global_params as gp


def prepay():
    (json, errors) = basic.prepay_validate()
    if errors:  # list is not empty
        return basic.resp(400, {"errors": errors})

    client = json["client"]
    items = json["items"]
    delivery_address = json["delivery_to"]

    if (not "pricelist" in json) or \
       (not "station" in json) or \
       (not "time" in json) or \
       (not "date" in json):
        return basic.resp(400, {"errors": "Haven't value"})

    with gp.db_conn() as db:
        client_count = 0
        client_id = None

        # Поиск клиента в базе
        if "id" not in client:
            client_count = 0
        else:
            client_count = int(
                    db.query(
                          "SELECT count(clientid) " +
                          "FROM root.client " +
                          "WHERE clientid = " + str(client["id"])
                            )[0][0]
                          )

        if client_count == 0:
            # Добавляем клиента если не находится

            insert = db.prepare(
                        "INSERT INTO root.client (name, phone, email, city, street, " +
                        "house, building, flat_office) " +
                        "VALUES ($1, $2, $3, $4, $5, $6, $7, $8) " +
                        "RETURNING clientid;")
            [(client_id,)] = insert(
                                   str(client["name"]) if "name" in client else "",
                                   str(client["phone"]) if "phone" in client else "",
                                   str(client["email"]) if "email" in client else "",
                                   str(client["city"]) if "city" in client else "",
                                   str(client["street"]) if "street" in client else "",
                                   str(client["house"]) if "house" in client else "",
                                   str(client["building"]) if "building" in client else "",
                                   str(client["flat_office"]) if "flat_office" in client else "")
        elif client_count == 1:
            client_id = str(client["id"])
        elif client_count > 1:
            return gp.resp(400, {"errors": "Multiple values"})

        items_accepted = []

        comment = ""

        for item in items:
            if "id" not in item:
                return gp.resp(400, {"errors": "Uncorrect value"})

            result = db.query("SELECT i.itemid, i.globalid, s.value, p.price " +
                              "FROM root.item i " +
                              "INNER JOIN root.store s ON s.globalid = i.globalid " +
                              "INNER JOIN root.price p ON p.globalid = i.globalid " +
                              "WHERE i.itemid = " + str(item["id"]) + " AND " +
                                    "p.pricelistid = " + str(json["pricelist"]) + " AND " +
                                    "s.stationid = " + str(json["station"]))
            if len(result) != 1:
                comment += "NoName " + item["store"] + "шт " + result[0]["price"] + " | "
                continue
            if float(item["store"]) > result[0]["value"]:
                comment += "NoName " + item["store"] + "шт " + result[0]["price"] + " | "
                continue

            items_accepted.append({
                              "itemid": result[0]["itemid"],
                              "globalid": result[0]["globalid"],
                              "store": item["store"],
                              "realprice": result[0]["price"],
                              "price": item["price"]
                             })

        insert = db.prepare(
            "INSERT INTO root.prepay (createtime, todate, totime, stationid, clientid, " +
            "createby, storn, sourceid, prepayclassid, prepaystateid) " +
            "VALUES ($1, $2, $3, $4, $5, 1, 1, 1, 1, 1) " +
            "RETURNING prepayid")

        prepay_id = None
        [(prepay_id,)] = insert(
            datetime.datetime.now(),
            datetime.datetime.strptime(json["date"], '%Y-%m-%d').date(),
            datetime.datetime.strptime(json["time"], '%H:%M').time(),
            int(json["station"]),
            int(client_id))

        for item in items_accepted:
            insert = db.prepare("SELECT public.calc_store_item($1, $2, $3, $4)")
            insert(int(item["itemid"]), int(item["globalid"]), float("{0:.3f}".format(float(item["store"]))), int(json["station"]))

            insert = db.prepare("INSERT INTO root.prepayitem(prepayid, itemid, amount, price, realprice, " +
                                                    "subtotal, total, stationid, globalid) " +
                                "VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)")
            insert(prepay_id, int(item["itemid"]), float(item["store"]), float(item["price"]), float(item["realprice"]),
                   float(item["price"]) * float(item["store"]), float(item["realprice"]) * float(item["store"]), int(json["station"]), int(item["globalid"]))

        insert = db.prepare(
                        "INSERT INTO root.prepayinfo (name, phone, city, street, house, " +
                                                 "building, flat_office, prepayid) " +
                        "VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ")

        insert(
            str(delivery_address["customer"]) if "customer" in client else "",
            str(delivery_address["customerphone"]) if "customerphone" in client else "",
            str(delivery_address["name"]) if "name" in client else "",
            str(delivery_address["phone"]) if "phone" in client else "",
            str(delivery_address["city"]) if "city" in client else "",
            str(delivery_address["street"]) if "street" in client else "",
            str(delivery_address["house"]) if "house" in client else "",
            str(delivery_address["building"]) if "building" in client else "",
            str(delivery_address["flat_office"]) if "flat_office" in client else "",
            prepay_id)

        insert = db.prepare("INSERT INTO root.prepaystatus(prepayid, paymentok, itemok, ready, send, received, cancell) " +
                            "VALUES($1, 0, 0, 0, 0, 0, 0)")
        insert(prepay_id)

        return gp.resp(200, {"id": str(prepay_id), "client": str(client_id)})
