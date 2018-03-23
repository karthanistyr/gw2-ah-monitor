import requests
from .exception import ApplicationError

class SessionHelper:
    """
    Creates an ambient TCP session that can be retrieved
    easily from anywhere in the code.
    """

    _ambient_session = None

    def __enter__(self):
        if(SessionHelper._ambient_session is None):
            #TODO: ugh; hacky -- also, we don't always want to use requests?
            SessionHelper._ambient_session = requests.Session()
        else:
            raise ApplicationError("There is already an ambient session.")
            
        # not too useful return (intended usage is `with SessionHelper():`)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        SessionHelper._ambient_session.close()
        SessionHelper._ambient_session = None

    def get_ambient_session():
        return SessionHelper._ambient_session
