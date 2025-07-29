# Python version: 3.10
import functions_framework

@functions_framework.http
def main(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        return 'No name in request!', 400 # Bad Request status code
    
    return f'Hello {name}!', 200