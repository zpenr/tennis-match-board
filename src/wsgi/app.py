import re
from urllib.parse import parse_qs

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
    
    def __call__(self, environ: dict, start_response):
        response_body = '404 NOT FOUND'
        status = '404 NOT FOUND'

        print(environ.get('wsgi.post_form'))

        path = environ.get('PATH_INFO','/')
        mask = re.compile(r'(<[A-Za-z]+>)')
        request_method = environ['REQUEST_METHOD']
        
        for route in self.routes[request_method]:
            
            new_mask = re.sub(mask,r'(?P\1[^/]+)',route)
            res = re.fullmatch(new_mask,path)
            if res:
                parametrs = res.groupdict()
                handler = self.routes[request_method][route]
                if request_method == 'POST':

                    content_length = int(environ.get('CONTENT_LENGTH',0))
                    request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
                    data = parse_qs(request_body)
                    response_body = handler(data)

                elif parametrs:
                    response_body = handler(parametrs)

                else:
                    response_body = handler()
                status = '200 OK'
                break
        
        if 'static' in path:
            headers = [('Content-Type', 'text/css')]
        else:
            headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]