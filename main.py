#!/usr/bin/env python3

import flask

import basic as basic
import global_params as gp

import get.check, get.client, get.group, get.item, get.price, get.prepay, get.store
import post.barcode, post.check, post.group, post.item, post.prepay, post.price, post.store


app = flask.Flask(__name__)

# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


##### PING #####
@app.route('/florapi/0.9/ping&key=' + gp.key,  methods=['GET'])
def ping():
    print('hello')
    return basic.resp(200, {"florapi": "Hello. I'm florapi."})


##### ЦЕНЫ #####
@app.route('/florapi/0.9/prices&key=' + gp.key, methods=['GET'])
def get_prices():
    return get.price.prices()


@app.route('/florapi/0.9/prices=<int:pricelist_id>&key=' + gp.key, methods=['GET'])
def get_prices_pricelist(pricelist_id):
    return get.price.prices_pricelist(pricelist_id)


@app.route('/florapi/0.9/prices=<int:pricelist_id>/<int:item_id>&key=' + gp.key, methods=['GET'])
def get_price(pricelist_id, item_id):
    return get.price.price(pricelist_id, item_id)


@app.route('/florapi/0.9/prices&key=' + gp.key,  methods=['POST'])
def add_price():
    return post.price.add_price()


##### ОСТАТКИ #####
@app.route('/florapi/0.9/stores&key=' + gp.key, methods=['GET'])
def get_stores():
    return get.store.stores()


@app.route('/florapi/0.9/stores=<int:station_id>&key=' + gp.key, methods=['GET'])
def get_stores_stantion(station_id):
    return get.store.stores_stantion(station_id)


@app.route('/florapi/0.9/stores=<int:station_id>/<int:item_id>&key=' + gp.key, methods=['GET'])
def get_store(station_id, item_id):
    return get.store.store(station_id, item_id)


@app.route('/florapi/0.9/stores&key=' + gp.key,  methods=['POST'])
def add_store():
    return post.store.add_store()

##### КЛИЕНТЫ #####
@app.route('/florapi/0.9/clients&key=' + gp.key, methods=['GET'])
def get_clients():
    return get.client.clients()


@app.route('/florapi/0.9/clients/<int:client_id>&key=' + gp.key, methods=['GET'])
def get_client(client_id):
    return get.client.client(client_id)


##### ТОВАРЫ #####
@app.route('/florapi/0.9/items&key=' + gp.key, methods=['GET'])
def get_items():
   return get.item.items()


@app.route('/florapi/0.9/items=<int:group_id>&key=' + gp.key, methods=['GET'])
def get_items_group(group_id):
    return get.item.items_group(group_id)


@app.route('/florapi/0.9/items/<int:item_id>&key=' + gp.key, methods=['GET'])
def get_item(item_id):
    return get.item.item(item_id)


##### ПРЕДЗАКАЗ #####
@app.route('/florapi/0.9/prepay&key=' + gp.key, methods=['POST'])
def post_prepay():
    return post.prepay.prepay()

@app.route('/florapi/0.9/prepay_status=<int:prepay_id>&key=' + gp.key, methods=['GET'])
def get_prepay_status():
   return get.prepay.prepay_status()

##### ГРУППЫ #####
@app.route('/florapi/0.9/groups&key=' + gp.key, methods=['GET'])
def get_groups():
   return get.group.groups()


@app.route('/florapi/0.9/groups&key=' + gp.key,  methods=['POST'])
def add_groups():
    return post.group.add_group()


##### ШТРИХКОДЫ #####
@app.route('/florapi/0.9/barcode&key=' + gp.key,  methods=['POST'])
def add_barcode():
    return post.barcode.add_barcode()


##### ЧЕКИ #####
@app.route('/florapi/0.9/checks&key=' + gp.key,  methods=['GET'])
def list_check():
    return get.check.checks_list()


@app.route('/florapi/0.9/check=<int:checkid>&key=' + gp.key,  methods=['GET'])
def get_check(checkid):
    return get.check.check_avaliable(str(checkid))


@app.route('/florapi/0.9/check=<int:checkid>&import=1&key=' + gp.key,  methods=['POST'])
def update_check(checkid):
    return post.check.check_import(str(checkid))

    
# ERROR
@app.errorhandler(400)
def page_not_found(e):
    return basic.resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return basic.resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return basic.resp(405, {})


# !!!!!! START !!!!!!
if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    #app.debug = False
    app.run(host=gp.host, port=gp.port)
