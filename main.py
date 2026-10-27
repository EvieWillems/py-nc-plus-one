from fastapi import FastAPI, requests

from routes.events import router as events_router

app = FastAPI(title='nc_plus_one_api')

app.include_router(events_router)

def response_formatter(endpoint):
    def wrapper():
        '''endpoints return tuple = (title,response), where response = ordered dict'''
        '''wrapper converts into readable json format''' 
        title_response = endpoint()
        return {title_response[0]:[{k:v for k,v in r.items()} for r in title_response[1]]}
    return wrapper