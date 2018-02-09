class Assert:
    """Provides some facilities for asserting on statements"""

    def expectexceptiontype(exception_type: type):
        """Will throw an AssertionError if an exception of the required type
        is not thrown by the decorated function."""

        def assert_wrapper(func):
            def run_func(self, *args, **kwargs):
                has_thrown = False
                try:
                    func(self, *args, **kwargs)
                except exception_type:
                    has_thrown = True
                except:
                    pass
                finally:
                    if(not has_thrown):
                        raise AssertionError("No exception of expected type" +
                            " ""{}"" was thrown.".format(exception_type))
            return run_func
        return assert_wrapper
