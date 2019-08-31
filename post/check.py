import postgresql

import basic as basic
import global_params as gp


def check_import(checkid):
    try:
        with postgresql.open(gp.dbconnect) as db:
            db.execute("UPDATE root.check SET exported = 1 "                              
                       "WHERE checkid = " + str(checkid))
    except:
        return basic.resp(400, {"errors": "Haven't connect with base"})
    return basic.resp(200, {})

