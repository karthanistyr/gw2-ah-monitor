import traceback

class Assert:
    """Provides some facilities for asserting on statements"""

    def expectexceptiontype(exception_type: type):
        """Will throw an AssertionError if an exception of the required type
        is not thrown by the decorated function."""

        def assert_wrapper(func):
            def run_func(self, *args, **kwargs):
                incidental_exception = None
                has_thrown = False
                try:
                    func(self, *args, **kwargs)
                except exception_type:
                    has_thrown = True
                except BaseException as e:
                    incidental_exception = e
                finally:
                    if(not has_thrown):
                        if(incidental_exception is not None):
                            raise AssertionError("The wrong exception type " +
                                "was thrown. Details: {}".format(traceback.format_exception(incidental_exception.__class__, incidental_exception, incidental_exception.__traceback__)))
                        else:
                            raise AssertionError("No exception of expected " +
                            "type ""{}"" was thrown.".format(exception_type))
            return run_func
        return assert_wrapper
