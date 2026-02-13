import re
class App():
    def __init__(self):
        self.routes = {}
    def route(self,path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO','/')
        mask = r'<[A-Za-z]+>'
        for route in self.routes:
            new_mask = re.sub(mask,'[^/]+',)
            res = re.fullmatch(new_mask,path)
        else:
            response_body = '404 NOT FOUND'
            status = '404 NOT FOUND'

        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]