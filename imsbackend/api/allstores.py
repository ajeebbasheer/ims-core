import json
from flask import request, Response, Blueprint
from imsbackend import LOGGER
from imsbackend.services import Service
from imsbackend.api.globals import Globals, HttpStatus, Status
from imsbackend.api.middleware import login_required
from flask import Flask, json, g, request
from flask_cors import cross_origin


SERVICE_CODE = "000"


bp = Blueprint('all', __name__, url_prefix='/api/all')


@bp.route('/init', methods=['POST'])
@cross_origin()
def init_all_stores():
    """
    REST API to initialize all stores.
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

    branches = service.find_all(Globals.BRANCH, identifier)
    income_types = service.find_all(Globals.TYPE, {"type": "INC"})
    expense_types = service.find_all(Globals.TYPE, {"type": "EXP"})

    if not branches:
        LOGGER.error("No branches fetched")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "No branches fetched"})
        return response

    LOGGER.debug(f"BRANCHES: {branches}")

    all_batches = []
    all_students = []
    batches_by_branch = {}
    students_by_branch = {}
    students_by_batch = {}

    try:
        for branch in branches:
            br_id = branch.get('_id')
            if br_id:
                identifier = {"branchId": br_id}
                batches = service.find_all(Globals.BATCH, identifier)
                all_batches += batches
                batches_by_branch[br_id] = batches
                students = service.find_all(Globals.STUDENT, identifier)
                all_students += students
                students_by_branch[br_id] = students
                for batch in batches:
                    batch_id = batch.get('_id')
                    if batch_id:
                        selector = {"batchId": batch_id}
                        students_by_batch[batch_id] = service.find_all(Globals.STUDENT, selector)

        response = response_generator(Globals.STATUS_OK, HttpStatus.HTTP_200,
                                      (SERVICE_CODE + __api_code +
                                       Status.SUCCESS_1000),
                                      Status.SUCCESS_1000_VALUE,
                                      {"status": "Fetch Successful",
                                       "branches": branches,
                                       "batches": all_batches,
                                       "batches_by_branch": batches_by_branch,
                                       "students": all_students,
                                       "students_by_branch": students_by_branch,
                                       "students_by_batch": students_by_batch,
                                       "income_types": income_types,
                                       "expense_types": expense_types})

    except Exception as excp:
        LOGGER.error(f"Exception in fetching data: {excp}")
        response = response_generator(Globals.STATUS_KO, HttpStatus.HTTP_500,
                                      (SERVICE_CODE + __api_code +
                                       Status.ERROR_4000),
                                      Status.ERROR_4000_VALUE,
                                      {"status": "Exception in fetching data"})

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
