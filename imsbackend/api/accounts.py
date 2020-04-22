import json
from flask import request, Response, Blueprint
from imsbackend import LOGGER
from imsbackend.services import Service
from imsbackend.api.globals import Globals, HttpStatus, Status
from imsbackend.api.middleware import login_required
from flask import Flask, json, g, request
from flask_cors import cross_origin


SERVICE_CODE = "004"

bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@bp.route('/gettypes', methods=['POST'])
@cross_origin()
def get_by_id_or_code():
    """
    REST API to get an entry.
    """

    __api_code = "002"
    response = None
    json_req_data = None

    source_ip = request.remote_addr

    LOGGER.debug("Received a request from source_ip = " + str(source_ip) +
                 ", type(source_ip) = " + str(type(source_ip)))

    request_size = request.content_length

    if request_size > Globals.MAX_UPLOAD_SIZE:
        LOGGER.error(f"Request bigger than max size {Globals.MAX_UPLOAD_SIZE}")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_404,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4002),
                                      Status.ERROR_4002_VALUE,
                                      {"status": "Request is bigger than max size",
                                       "input size": request_size})
        return response

    try:
        json_req_data = request.get_json()

    except Exception as excp:
        LOGGER.error(f"Bad request: {excp}")
        json_req_data = None

    if not json_req_data:
        LOGGER.error("No JSON input data provided")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_404,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4004),
                                      Status.ERROR_4004_VALUE,
                                      {"status": "Server could not understand the request"})
        return response

    LOGGER.debug(f"input json: {json_req_data}")

    student_id = json_req_data.get("_id")

    if not student_id:
        LOGGER.error("Input value missing")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_401, SERVICE_CODE +
                                      __api_code + Status.ERROR_4001,
                                      Status.Status.ERROR_4001_VALUE,
                                      {"error": Status.Status.ERROR_4001_VALUE})
        return response

    service = Service()

    if not service.db_client:
        LOGGER.error(f"Unable to do get mongo client")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "Unable to connect MongoDB"})
        return response

    LOGGER.info(f"Connected to mongo: {service.db_client}")

    identifier = {"_id": student_id}

    result = service.find_one(Globals.STUDENT, identifier)

    if not result:
        LOGGER.error("Fetch failed")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": f"No batch found with id: {identifier}"})
        return response

    response = response_generator(Globals.STATUS_OK, HttpStatus.HTTP_200,
                                  (SERVICE_CODE + __api_code +
                                   Status.SUCCESS_1000),
                                  Status.SUCCESS_1000_VALUE,
                                  {"status": "Fetch Successful",
                                   "data": result})

    return response


@bp.route('/addtype', methods=['POST'])
@cross_origin()
def add_type():
    """
    REST API to get an entry.
    """

    __api_code = "003"
    response = None
    json_req_data = None

    source_ip = request.remote_addr

    LOGGER.debug("Received a request from source_ip = " + str(source_ip) +
                 ", type(source_ip) = " + str(type(source_ip)))

    request_size = request.content_length

    if request_size > Globals.MAX_UPLOAD_SIZE:
        LOGGER.error(f"Request bigger than max size {Globals.MAX_UPLOAD_SIZE}")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_404,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4002),
                                      Status.ERROR_4002_VALUE,
                                      {"status": "Maximum size reached", "input size": request_size})
        return response

    try:
        json_req_data = request.get_json()
    except Exception as excp:
        LOGGER.error(f"Bad request: {excp}")
        json_req_data = None

    if not json_req_data:
        LOGGER.error("No JSON input data provided")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_404,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4004),
                                      Status.ERROR_4004_VALUE,
                                      {"status": "Server could not understand the request"})
        return response

    LOGGER.debug(f"input json: {json_req_data}")

    tag_type = json_req_data.get("type")
    name = json_req_data.get("name")
    tag = json_req_data.get("tag")

    if (not tag_type) or (not name) :
        LOGGER.error("Input value missing")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_401, SERVICE_CODE +
                                      __api_code + Status.ERROR_4001,
                                      Status.Status.ERROR_4001_VALUE,
                                      {"status": Status.Status.ERROR_4001_VALUE})
        return response

    service = Service()

    if not service.db_client:
        LOGGER.error(f"Unable to do get mongo client")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "Unable to connect MongoDB"})
        return response

    LOGGER.info(f"Connected to mongo: {service.db_client}")

    data_dict = {
                 "type": tag_type,
                 "name": name,
                 "tag": tag,
    }

    result = service.insert_one(Globals.TYPE, data_dict)

    if not result:
        LOGGER.error("Insert failed")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_200,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "Unable to insert to MongoDB"})
        return response

    if not result.get('inserted_id'):
        LOGGER.error("Inserted id not returned")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "inserted_id not returned"})
        return response

    data_dict['_id'] = result.get('inserted_id')

    response = response_generator(Globals.STATUS_OK, HttpStatus.HTTP_200,
                                  (SERVICE_CODE + __api_code +
                                   Status.SUCCESS_1000),
                                  Status.SUCCESS_1000_VALUE,
                                  {"status": "Insert Successful",
                                   "data": data_dict})

    return response


def response_generator(status, http_code, output_code, output_value, data):
    """Returns a HTTP response with JSON data"""

    return_value = {
        'status': status,
        'statusCode': output_code,
        'statusValue': output_value,
        'data': data
    }

    json_return_value = json.dumps(return_value)

    response = Response(json_return_value, status=http_code,
                        mimetype=Globals.MIMETYPE_JSON)

    LOGGER.info("printing return_value ")
    LOGGER.info(return_value)

    return response
