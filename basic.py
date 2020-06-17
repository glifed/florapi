import flask
import json

def price_validate():
    errors = []
    json = flask.request.get_json()

    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    return (json, errors)


def store_validate():
    errors = []
    json = flask.request.get_json()

    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    return (json, errors)

def group_validate():
    errors = []
    json = flask.request.get_json()

    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    return (json, errors)


def group_validate():
    errors = []
    json = flask.request.get_json()

    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    return (json, errors)


def barcode_validate():
    errors = []
    json = flask.request.get_json()

    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    return (json, errors)



def prepay_validate():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    for field_name in ['pricelist', 'station']:
        if type(json.get(field_name)) is not str:
            errors.append(
                "Field '{}' is missing or is not a string".format(field_name)
            )

    return (json, errors)

def to_json(data):
    return json.dumps(data, ensure_ascii=False) + "\n"

def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data),
    )
