def response_formatter(endpoint):
    def wrapper():
        '''endpoints return tuple = (title,response), where response = ordered dict'''
        '''wrapper converts into readable json format''' 
        title_response = endpoint()
        return {title_response[0]:[{k:v for k,v in r.items()} for r in title_response[1]]}
    return wrapper