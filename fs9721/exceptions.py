class DmmException(Exception):
    "Base exception class for Dmm."


class DmmNoData(DmmException):
    "Read from serial port timed out with no bytes read."


class DmmInvalidSyncValue(DmmException):
    "Got an invalid byte during syncronization."


class DmmReadFailure(DmmException):
    "Unable to get a successful read within the number of allowed retries."
