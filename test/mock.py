import inspect
from enum import Enum

class MemberNotSetupError(Exception):
    """Should be thrown when a mocked class member was accessed without
    having been setup before, i.e. when the behaviour was not defined."""

    def __init__(self, member_name):
        super().__init__("This member was not setup in strict mode: {}".format(member_name))

def _pass_through_method():
    """Returns a function pointer for a function simply calling pass."""
    def _pass(*args, **kwargs):
        pass
    return _pass

def _return_expression(expression):
    """Returns a function pointer for a function returning the result of an
    arbitrary expression."""

    def _return(*args, **kwargs):
        return expression
    return _return

def _throw_exception(exception: Exception):
    """Returns a function pointer for a function throwing an arbitrary
    exception"""

    def _throw(*args, **kwargs):
        raise exception
    return _throw

def _throw_member_not_setup_exception(member_name):
    """Returns a function pointer to a function throwing the
    MemberNotSetupError exception."""

    return _throw_exception(MemberNotSetupError(member_name))

def _override_property_by_name(obj, property_name, getter):
    if(callable(getattr(obj, property_name))):
        raise ArgumentValidationError("{} is not a field or property name on" +
            " object of type {}".format(property_name, obj.__class__))
    setattr(obj.__class__, property_name,
        property(fget=getter, fset=lambda self, value: value))

def _override_member_by_name(obj, member_name, replacement):
    if(not callable(getattr(obj, member_name))):
        _override_property_by_name(obj, member_name, replacement)
    else:
        setattr(obj, member_name, replacement)

def _override_all_members_with_throw(obj, excluded_names=None):
    for member_name in obj.__dict__:
        if(excluded_names is None or member_name not in excluded_names):
            _override_member_by_name(obj, member_name,
                _throw_member_not_setup_exception(member_name))

class MockMode(Enum):
    """Mock object members behaviour.
    Loose means that members without an explicit setup will behave identically
    to the members of the same name on the target class.
    Strict means that any member without an explicit setup will throw an
    exception upon being called (this forces the developer to fully
    specify their mock behaviours)."""

    Strict = "Strict"
    Loose = "Loose"

class Mock:
    """Provides an interface for mocking a type and setting up mocked
    member behaviour, i.e. returning something or throwing an exception"""
    def __init__(self, cls, mode: MockMode=MockMode.Strict):
        self.mocked_class = cls
        self.setups = {}
        self.mode = mode

    def setup(self, class_member_name):
        stp = MockedMember(class_member_name)
        self.setups[class_member_name] = stp
        return stp

    def object(self):
        proxy_type = type("__{}_Proxy__".format(self.mocked_class.__qualname__), (self.mocked_class,), {})
        #forcing argument-less ctor
        _override_member_by_name(proxy_type, "__init__", _pass_through_method())

        mock = proxy_type()
        if(self.mode == MockMode.Strict):
            _override_all_members_with_throw(mock,
                excluded_names={"__init__"}.update(self.setups.keys()))

        for st in self.setups:
            _override_member_by_name(mock, st, self.setups[st]._code)

        return mock

class MockedMember:
    """Mock member behaviour. Provides an interface for specifying how a given
    mocked member should behave."""

    def __init__(self, cls_member):
        self.mocked_member = cls_member
        self._code = _throw_member_not_setup_exception(cls_member)

    def returns(self, expression):
        self._code = _return_expression(expression)

    def throws(self, exception: Exception):
        self._code = _throw_exception(exception)
