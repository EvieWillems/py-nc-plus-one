class InvalidLoginException(Exception):
    def __init__(self,status_code=401,detail='invalid email or password'):
        self.status_code = status_code
        self.detail = detail

class ExistingUserException(Exception):
    def __init__(self,status_code=409,detail='user with that email already exists'):
        self.status_code = status_code
        self.detail = detail

class RSVPConflictException(Exception):
    def __init__(self,status_code=409,event_id=None):
        self.status_code = status_code
        self.detail = f'user has already rsvpd to event {event_id}'