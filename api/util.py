def getResponseHeaders():
    return {
        'Access-Control-Allow-Origin':'*'
    }

def get_user_id(headers):
    return headers.get('app_user_id')

def get_user_name(headers):
    return headers.get('app_user_name')
