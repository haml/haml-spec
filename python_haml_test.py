from __future__ import print_function, unicode_literals

import json

from collections import OrderedDict
from hamlpy import compiler


num_pass, num_fail, num_error = 0, 0, 0

with open('tests.json') as f:
    tests = json.load(f, object_pairs_hook=OrderedDict)
    for category, category_tests in tests.items():
        print(category)
        for description, test in category_tests.items():
            try:
                html = compiler.Compiler(options=test.get('config')).process(test['haml']).strip()
                if html == test['html']:
                    print(" > %s: OK" % description)
                    num_pass += 1
                else:
                    print(" > %s: FAIL" % description)
                    print("    - Expected: %s" % test['html'].replace('\n', '\\n'))
                    print("    - Actual  : %s" % html.replace('\n', '\\n'))
                    num_fail += 1
            except Exception as e:
                print(" > %s: ERROR" % description)
                print("    - Exception: %s" % str(e))
                num_error += 1

print("==== Passed: %d, Failed: %d, Errors: %d ====" % (num_pass, num_fail, num_error))
