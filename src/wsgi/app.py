import re
from urllib.parse import parse_qs
class Redirect():
    def __init__(self, redirect_link):
        self.redirect_link = redirect_link
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
    
    def _dict_values_to_elem(self, dict: dict)->dict:
        redict = {}
        for key in dict.keys():
            redict[key] = dict[key][0]
        return redict
    
    def __call__(self, environ: dict, start_response):
        response_body = '404 NOT FOUND'
        status = '404 NOT FOUND'
        parametrs = {}

        path = environ.get('PATH_INFO','/')
        mask = re.compile(r'(<[A-Za-z]+>)')

        request_method = environ['REQUEST_METHOD']
        query_string = environ['QUERY_STRING']

        for route in self.routes[request_method]:
            
            new_mask = re.sub(mask,r'(?P<\1>[^/]+)',route)
            res = re.fullmatch(new_mask,path)
            if res:

                parametrs.update(res.groupdict())
                handler = self.routes[request_method][route]

                if request_method == 'POST':
                    content_length = int(environ.get('CONTENT_LENGTH',0))
                    request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
                    parametrs.update(self._dict_values_to_elem(parse_qs(request_body)))
                    

                if query_string:
                    parametrs.update(self._dict_values_to_elem(parse_qs(query_string)))

                if parametrs:
                        response_body = handler(**parametrs)

                else:
                    response_body = handler()
                
                status = '200 OK'
                break

        if 'static' in path:
            headers = [('Content-Type', 'text/css')]
        else:
            headers = [('Content-Type', 'text/html; charset=utf-8')]
        if isinstance(response_body, Redirect):
            status = '302 Redirect'
            headers = [('Location', response_body.redirect_link)]
            response_body = ''
        
        start_response(status, headers)

        return [response_body.encode('utf-8')]