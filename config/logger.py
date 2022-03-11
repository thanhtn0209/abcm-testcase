import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        # get necessary information for logger
        log_info = {
            'level': record.levelname,
            'ts': datetime.fromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S:%f"),
            "caller": record.pathname + ":" + str(record.lineno),
            "msg": record.msg
        }

        # format message log to json
        record.msg = json.dumps(log_info)

        return super().format(record)


try:
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)
    loggingStreamHandler = logging.FileHandler('aolf.log')
    loggingStreamHandler.setFormatter(JSONFormatter())
    LOGGER.addHandler(loggingStreamHandler)
except Exception as e:
    raise e
