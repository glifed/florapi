import postgresql

import basic as basic
import global_params as gp

def clients():
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT clientid, name, phone, email, city, street, house, building, flat_office, card "
                          "FROM root.client "
                          "WHERE avaliable = 1")
        clients = []
        for (clientid, name, phone, email, city, street, house, building, flat_office, card) in tuples:
            clients.append({ "id": clientid, "name": name, "phone": phone, "email": email, "city": city,
                             "street": street, "house": house, "building": building, "flat_office": flat_office, "card": card })
        return basic.resp(200, {"clients": clients})


def client(client_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT clientid, name, phone, email, city, street, house, building, flat_office, card "
                          "FROM root.client "
                          "WHERE avaliable = 1 AND clientid = " + str(client_id))
        clients = []
        for (clientid, name, phone, email, city, street, house, building, flat_office, card) in tuples:
            clients.append({ "id": clientid, "name": name, "phone": phone, "email": email, "city": city,
                             "street": street, "house": house, "building": building, "flat_office": flat_office, "card": card })
        return basic.resp(200, {"clients": clients})