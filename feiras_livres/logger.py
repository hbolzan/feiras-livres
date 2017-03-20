import json
import datetime
from logging import Formatter


class LogstashFormatter(Formatter):
    def __init__(self, task_name=None):
        self.task_name = task_name

        super(LogstashFormatter, self).__init__()

    def format(self, record):
        if not record.args:
            data = self.get_middleware_data(record)
        else:
            try:
                args = record.args[0].split(' ')
            except:
                return

            data = {
                "severity": record.levelname,
                "method": args[0],
                "path": args[1],
                "time": record.created,
                "status": record.status_code,
                "@timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            }

        return json.dumps(data)

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
