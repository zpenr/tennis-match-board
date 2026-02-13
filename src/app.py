import re
class App():
    def __init__(self):
        self.routes = {
            'GET':{},
            'POST':{},
            'PATCH':{},
            'DELETE':{},
            'PUT':{},
            'HEAD':{},
            'OPTIONS':{}
            }

    def route(self,path: str, request_method: str = 'GET'):
        def wrapper(handler):
            self.routes[request_method][path] = handler
            return handler
        return wrapper
    
    def __call__(self, environ, start_response):
        response_body = '404 NOT FOUND'
        status = '404 NOT FOUND'

        path = environ.get('PATH_INFO','/')
        mask = r'(<[A-Za-z]+>)'
        request_method = environ['REQUEST_METHOD']
        
        for route in self.routes[request_method]:
            new_mask = re.sub(mask,r'(?P\1[^/]+)',route)
            res = re.fullmatch(new_mask,path)
            if res:
                parametrs = res.groupdict()
                handler = self.routes[request_method][route]
                if parametrs:
                    response_body = handler(parametrs)
                else:
                    response_body = handler()
                status = '200 OK'
                break

        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]