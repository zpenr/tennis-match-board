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
    
    def query_string_to_dict(self,query_string: str) -> dict:
        parametrs_dict = dict()
        parametrs = query_string.split('&')
        for param in parametrs:
            title_value = param.split('=$')
            parametrs_dict[title_value[0]] = title_value[1]
        return parametrs_dict
    
    def __call__(self, environ: dict, start_response):
        response_body = '404 NOT FOUND'
        status = '404 NOT FOUND'
        parametrs = None

        path = environ.get('PATH_INFO','/')
        mask = re.compile(r'(<[A-Za-z]+>)')

        request_method = environ['REQUEST_METHOD']
        query_string = environ['QUERY_STRING']

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
                    

                if query_string:
                    response_body = handler(self.query_string_to_dict(query_string))

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