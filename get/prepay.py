import postgresql

import basic as basic
import global_params as gp


def prepay_status(prepay_id):
    with postgresql.open(gp.dbconnect) as db:
        tuples = db.query("SELECT ps.name, pp.prepaystateid " 
                          "FROM root.prepay pp "
                          "INNER JOIN root.prepaystate ps "
                          "ON pp.prepaystateid = ps.prepaystateid "
                          "WHERE prepayid = " + str(prepay_id))
        prepay_state = []
        for (name, prepaystateid) in tuples:
            prepay_state.append({ "name": name, "state_id": prepaystateid })
        return basic.resp(200, {"prepay": prepay_state})