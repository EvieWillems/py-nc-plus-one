from typing import Optional

def response_formatter(endpoint):
    def wrapper():
        '''endpoints return tuple = (title,response), where response = ordered dict'''
        '''wrapper converts into readable json format''' 
        title_response = endpoint()
        return {title_response[0]:[dict(r) for r in title_response[1]]}
    return wrapper

def response_formatter_args(endpoint):
    def wrapper(*args):
        '''endpoints return tuple = (title,response), where response = ordered dict'''
        '''wrapper converts into readable json format''' 
        title_response = endpoint(*args)
        return {title_response[0]:[dict(r) for r in title_response[1]]}
    return wrapper