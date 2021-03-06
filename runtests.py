import traceback
from gw2ahmonitor.test.fixture import TestRunner, TestStatusEnum
from gw2ahmonitor.test.rest.clienttests import *
from gw2ahmonitor.test.rest.endpointstests import *
from gw2ahmonitor.test.helpers.assertstests import *
from gw2ahmonitor.test.helpers.exceptiontests import *
from gw2ahmonitor.test.helpers.mathtests import *
from gw2ahmonitor.test.helpers.sessiontests import *
from gw2ahmonitor.test.storage.storagetests import *

classes_to_test = [
    ClientTests,
    EndpointCallTests,
    PaginatedEndpointTests,
    PricesEndpointTests,
    AssertTests,
    ExceptionTests,
    MathTests,
    SessionHelperTests,
    StorageTests
    ]

runner = TestRunner()

results = {}
for testclass in classes_to_test:
    results[testclass] = runner.run_from_class(testclass)

print("Tested {} test classes.".format(len(classes_to_test)))
for result in results:
    nb_passed = 0
    failures = []
    for test in results[result]:
        if(test.status == TestStatusEnum.Pass):
            nb_passed += 1
        if(test.status == TestStatusEnum.Fail):
            failures.append(test)
    print("{}: {} passed, {} failed.".format(result.__name__,
        nb_passed, len(failures)))
    for failure in failures:
        ex_string = traceback.format_exception(failure.exception.__class__,
            failure.exception, failure.exception.__traceback__)
        print("{}: failed with: ""{}""".format(failure.func_name,
            "".join(ex_string)))
