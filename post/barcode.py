import postgresql

import basic as basic


def add_barcode():
    (json, errors) = basic.barcode_validate()

    if errors:
        return basic.resp(400, {"errors": errors})

    barcode = json['barcode']

    for item in barcode:
        if (not 'code' in item) or \
           (not 'barc' in item):
            return basic.resp(400, {"errors": "Haven't value"})
        else:
            try:
                with postgresql.open(basic.dbconnect) as db:
                    id_item = db.query("SELECT itemid FROM root.barcode "                                       
                                       "WHERE barcode = '" + str(item['barc']) + "'")
                    if id_item == []:
                        db.query(str("INSERT INTO root.barcode(itemid, barcode) "
                                     "VALUES((SELECT itemid FROM root.item "
                                           "WHERE importcode = '{0}'), '{1}')"
                                    ).format(str(item['code']), str(item['barc'])))
                    else:
                        id_barc = db.query("SELECT barcodeid FROM root.barcode "                                       
                                       "WHERE barcode = '" + str(item['barc']) + "'")
                        db.query("UPDATE root.barcode SET itemid = " + id_item[0][0] + " "                                       
                                       "WHERE barcodeid = " + str(id_barc[0][0]))    
            except:
                return basic.resp(400, {"errors": "Haven't connect with base"})

    return basic.resp(200, {})
