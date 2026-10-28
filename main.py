from fastapi import FastAPI, requests, HTTPException



from routes.events import router as events_router
from routes.auth import router as auth_router

app = FastAPI(title='nc_plus_one_api')

app.include_router(events_router)
app.include_router(auth_router)