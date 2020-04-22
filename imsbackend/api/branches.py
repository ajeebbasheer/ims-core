import json
from flask import request, Response, Blueprint
from imsbackend import LOGGER
from imsbackend.services import Service
from imsbackend.api.globals import Globals, HttpStatus, Status
from imsbackend.api.middleware import login_required
from flask import Flask, json, g, request
from flask_cors import cross_origin



SERVICE_CODE = "001"

bp = Blueprint('branches', __name__, url_prefix='/api/branches')


@bp.route("/")
def helloWorld():
    LOGGER.info("HELLO WORLD")
    return "Hello, cross-origin-world!"


@bp.route('/loadall', methods=['POST'])
@cross_origin()
def load_all():
    """
    REST API to get an entry.
    """

    __api_code = "000"
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

    branch_id = json_req_data.get("_id")

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

    if branch_id:
        identifier = {"_id": branch_id}
    else:
        identifier = None

    branch_list = service.find_all(Globals.BRANCH, identifier)

    if not branch_list:
        LOGGER.error("No branches fetched")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "No branches fetched"})
        return response

    LOGGER.debug(f"BRANCHES: {branch_list}")

    batch_dict = {}

    for branch in branch_list:
        if branch.get('_id') and branch.get('code'):
            batches = service.find_all(Globals.BATCH, {"branchId": branch.get('_id')})
            batch_dict[branch.get('code')] = batches

    response = response_generator(Globals.STATUS_OK, HttpStatus.HTTP_200,
                                  (SERVICE_CODE + __api_code +
                                   Status.SUCCESS_1000),
                                  Status.SUCCESS_1000_VALUE,
                                  {"status": "Fetch Successful",
                                   "branch_list": branch_list,
                                   "batch_dict": batch_dict})

    return response


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

    branch_id = json_req_data.get("_id")

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

    if branch_id:
        identifier = {"_id": branch_id}
    else:
        identifier = None

    result = service.find_all(Globals.BRANCH, identifier)

    if not result:
        LOGGER.error("No branches fetched")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "No branches fetched"})
        return response

    response = response_generator(Globals.STATUS_OK, HttpStatus.HTTP_200,
                                  (SERVICE_CODE + __api_code +
                                   Status.SUCCESS_1000),
                                  Status.SUCCESS_1000_VALUE,
                                  {"status": "Fetch Successful",
                                   "branch_list": result})

    return response


@bp.route('/getbranch', methods=['POST'])
@cross_origin()
def get_by_id_or_ode():
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

    branch_id = json_req_data.get("_id")
    branch_code = json_req_data.get("code")

    if (not branch_id) and (not branch_code) :
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

    if branch_id:
        identifier = {"_id": branch_id}
    elif branch_code:
        identifier = {"code": branch_code}
    else:
        pass

    result = service.find_one(Globals.BRANCH, identifier)
    LOGGER.info("HERE")

    if not result:
        LOGGER.error("Insert failed")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": f"No branch found with id: {identifier}"})
        return response

    response = response_generator(Globals.STATUS_OK, HttpStatus.HTTP_200,
                                  (SERVICE_CODE + __api_code +
                                   Status.SUCCESS_1000),
                                  Status.SUCCESS_1000_VALUE,
                                  {"status": "Fetch Successful",
                                   "data": result})

    return response


@bp.route('/addbranch', methods=['POST'])
@cross_origin()
def add_branch():
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
    address = json_req_data.get("address")
    country = json_req_data.get("country")
    state = json_req_data.get("state")
    city = json_req_data.get("city")
    pin = json_req_data.get("pin")
    email = json_req_data.get("email")
    phone = json_req_data.get("phone")
    rent = json_req_data.get("rent")
    income = json_req_data.get("income")
    expense = json_req_data.get("expense")
    students = json_req_data.get("noOfStudents")
    fee_status = json_req_data.get("feeStatus")

    if (not name) or (not code):
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
                 "name": name,
                 "code": code,
                 "address": {"address": address,
                             "country": country,
                             "state": state,
                             "city": city,
                             "pin": pin },
                 "phone": phone,
                 "email": email,
                 "rent": rent,
                 "income": income,
                 "expense": expense,
                 "noOfStudents": students,
                 "feeStatus": fee_status,
                 "visibility": False}

    result = service.insert_one(Globals.BRANCH, data_dict)

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
