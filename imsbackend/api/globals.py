
class HttpStatus:
    HTTP_200 = 200  # Success
    HTTP_404 = 404  # Bad request
    HTTP_401 = 401  # None or bad credentials sent
    HTTP_500 = 500  # General internal server error


class Status:
    # Success codes
    SUCCESS_1000 = "1000"
    SUCCESS_1000_VALUE = "Command execution successful"

    # Error codes
    ERROR_4000 = "4000"
    ERROR_4000_VALUE = "Exception occured in the server. Command not successful"
    ERROR_4001 = "4001"
    ERROR_4001_VALUE = "Could not find JSON key"
    ERROR_4002 = "4002"
    ERROR_4002_VALUE = "Request bigger than max upload size"
    ERROR_4003 = "4003"
    ERROR_4003_VALUE = "Input validation failed"
    ERROR_4004 = "4004"
    ERROR_4004_VALUE = "Bad Request"


class Globals:
    TYPE = "incomeExpenseType"
    INCOME = "income"
    STUDENT = "students"
    FACULTY = "faculties"
    SUBJECT = "subjects"
    SUBJECT_CLASS = "subjectClasses"
    BATCH = "batches"
    STAFF = "nonTeachingStaffs"
    BRANCH = "branches"
    ONGOING = "On Going"
    ONHOLD = "On Hold"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    MAX_UPLOAD_SIZE = 10485760  # Maximum input size restricted to 10MB
    STATUS_OK = "OK"
    STATUS_KO = "KO"
    MIMETYPE_JSON = 'application/json'