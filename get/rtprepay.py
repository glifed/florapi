import postgresql
import basic as basic
import global_params as gp


def rtprepays():
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT  p.closetime, p.prepayid, us.name as username, "
                          "i.customer, i.customerphone, i.name, i.phone, i.city, "
                          "i.street, i.house, i.building, i.flat_office, i.comment, "
                          "pp.total, p.todate, p.totime, sum(ppi.total) as totalsum "
                          "FROM root.prepay p "
                          "INNER JOIN root.prepayinfo i ON i.prepayid = p.prepayid "
                          "LEFT OUTER JOIN root.prepaypayment pp ON i.prepayid = pp.prepayid "
                          "LEFT OUTER JOIN root.prepayitem ppi on i.prepayid = ppi.prepayid "
                          "INNER JOIN root.users us ON us.usersid = p.createby "
                          "WHERE p.closetime IS NULL "
                          "GROUP BY p.prepayid, p.closetime, us.name, i.name, "
                          "i.customer, i.customerphone, i.phone, i.city, "
                          "i.street, i.house, i.building, i.flat_office, "
                          "i.comment, pp.total, p.todate, p.totime "
                          "ORDER BY p.todate, p.totime")
        rtprepays = []
        for ( closetime, prepayid, username, customer, customerphone, name, phone, city, street, house, building, flat_office, comment, total, todate, totime, totalsum) in tuples:
            rtprepays.append({ "prepayid": prepayid, "username": username, "customer": customer, "customerphone": customerphone, "name": name, "phone": phone, "city": city, "street": street, "house": house, "building": building, "flat_office": flat_office, "comment": comment, "total": str(total), "todate": str(todate), "totime": str(totime), "totalsum": str(totalsum) })
        return basic.resp(200, {"rtprepays": rtprepays})
        
