import json
from flask import request, Response, Blueprint
from imsbackend import LOGGER
from imsbackend.services import Service
from imsbackend.api.globals import Globals, HttpStatus, Status
from imsbackend.api.middleware import login_required
from flask import Flask, json, g, request
from flask_cors import cross_origin



SERVICE_CODE = "002"

bp = Blueprint('batches', __name__, url_prefix='/api/batches')


@bp.route('/getall', methods=['POST'])
@cross_origin()
def get_all():
    """
    REST API to get an entry.
    """

    __api_code = "001"
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

    batch_id = json_req_data.get("_id")
    branch_id = json_req_data.get("branchId")

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

    if batch_id:
        identifier = {"_id": batch_id}
    else:
        identifier = {"branchId": branch_id}

    result = service.find_all(Globals.BATCH, identifier)

    if not result:
        LOGGER.error("No batches fetched")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "No batches fetched"})
        return response

    response = response_generator(Globals.STATUS_OK, HttpStatus.HTTP_200,
                                  (SERVICE_CODE + __api_code +
                                   Status.SUCCESS_1000),
                                  Status.SUCCESS_1000_VALUE,
                                  {"status": "Fetch Successful",
                                   "data": result})

    return response


@bp.route('/getbatch', methods=['POST'])
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

    batch_id = json_req_data.get("_id")
    batch_code = json_req_data.get("code")

    if (not batch_id) and (not batch_code) :
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

    if batch_id:
        identifier = {"_id": batch_id}
    elif batch_code:
        identifier = {"code": batch_code}
    else:
        pass

    result = service.find_one(Globals.BATCH, identifier)

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


@bp.route('/addbatch', methods=['POST'])
@cross_origin()
def add_batch():
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

    name = json_req_data.get("name")
    code = json_req_data.get("code")
    branch_id = json_req_data.get("branch")
    fee = json_req_data.get("fee")

    if (not name) or (not code) or (not branch_id):
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

    branch = service.find_one(Globals.BRANCH, {'_id': branch_id})

    LOGGER.info(f"BRANCH DETAILS: {branch}")

    data_dict = {
                 "name": name,
                 "code": code,
                 "branchId": branch_id,
                 "branch": branch,
                 "fee": fee
    }

    result = service.insert_one(Globals.BATCH, data_dict)

    if not result:
        LOGGER.error("Insert failed")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
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
