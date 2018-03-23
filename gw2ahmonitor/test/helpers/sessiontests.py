from ..fixture import TestClassBase, testmethod
from ...helpers.asserts import Assert
from ...helpers.exception import ApplicationError
from ...helpers.session import *

class SessionHelperTests(TestClassBase):

    @testmethod
    def T_context_create_AmbientSessionCreated(self):
        # arrange / act
        with SessionHelper():
            # assert
            session = SessionHelper.get_ambient_session()
            assert session is not None
            # TODO: assert on the type?

    @testmethod
    def T_context_create_AmbientSessionDestroyed(self):
        # arrange / act
        with SessionHelper():
            # assert
            session = SessionHelper.get_ambient_session()

        assert SessionHelper.get_ambient_session() is None

    @testmethod
    @Assert.expectexceptiontype(ApplicationError)
    def T_context_create_NestedAmbientSession_Throws(self):
        # arrange / act
        with SessionHelper():
            with SessionHelper():
                pass # boom
