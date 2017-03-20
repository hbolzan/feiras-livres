import json
import datetime
from logging import Formatter


class LogsJsonFormatter(Formatter):
    def __init__(self, task_name=None):
        self.task_name = task_name

        super(LogsJsonFormatter, self).__init__()

    def format(self, record):
        try:
            if not record.args:
                data = self.get_middleware_data(record)
            else:
                data = self.get_logger_data(record)
        except:
            return ""

        if data:
            return json.dumps(data)

    def get_logger_data(self, record):
        return {
            "severity": record.levelname,
            "method": args[0],
            "path": args[1],
            "time": record.created,
            "status": record.status_code,
            "@timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }

    def get_middleware_data(self, record):
        log_data = json.loads(record.msg)
        request = log_data["request"]
        response = log_data["response"]
        return {
            "severity": "INFO",
            "method": request["method"],
            "path": request["path"],
            "time": record.created,
            "status": response["status"],
            "request_body": request["body"],
            "@timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
