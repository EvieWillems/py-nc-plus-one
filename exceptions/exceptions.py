class InvalidLoginException(Exception):
    def __init__(self,status_code=404,detail='invalid email or password'):
        self.status_code = status_code
        self.detail = detail