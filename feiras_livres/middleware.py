import json
import logging

request_logger = logging.getLogger('django.request')


class LoggingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        _request_data = {
            "path": request.path,
            "method": request.method,
            "body": request.body,
            "remote_addr": request.META["REMOTE_ADDR"],
        }

        response = self.get_response(request)

        _response_data = {
            "status": response.status_code,
            "content": response.content,
        }

        log_data = {
            "request": _request_data,
            "response": _response_data
        }

        request_logger.info(json.dumps(log_data))

        return response

