import postgresql

import basic as basic
import global_params as gp


def checks_list():
    try:
        with postgresql.open(gp.dbconnect) as db:
            checks = db.query("SELECT checkid "
                              "FROM root.check "
                              "WHERE storn <> 1 AND exported <> 1 AND operationid = 1")
            items = []
            for checkid in checks:
                items.append({"checkid": str(checkid[0])})
            return basic.resp(200, {"checks": items})
    except:
        return basic.resp(400, {"errors": "Haven't connect with base"})


def check_avaliable(checkid):
    try:
        with postgresql.open(gp.dbconnect) as db:

            check = db.query("SELECT i.importcode, ci.amount, ci.price "
                             "FROM root.checkitem ci "
                             "INNER JOIN root.item AS i ON i.globalid = ci.globalid "
                             "WHERE ci.checkid = " + str(checkid))
            items = []
            for (code, count, price) in check:
                if not code:
                    code = "0"
                items.append({"code": str(code), "count": float(count), "price": float(price)})

            items_p = []
            payments = db.query("SELECT paymentid, SUM(total) "
                                "FROM root.checkpayment "
                                "WHERE checkid = " + str(checkid) + " "
                                                                    "GROUP BY paymentid")

            for (payment, total) in payments:
                items_p.append({"payment": int(payment), "total": float(total)})
    except:
        return basic.resp(400, {"errors": "Haven't connect with base"})

    answer = dict({"items": items, "payments": items_p})
    return basic.resp(200, {"check": answer})
