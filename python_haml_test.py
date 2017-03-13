from __future__ import print_function, unicode_literals

import json

from collections import OrderedDict
from hamlpy import compiler


def run_test(test, description):
    try:
        html = compiler.Compiler(options=test.get('config')).process(test['haml'])
        error = None
    except Exception as e:
        html = ''
        error = e

    if html.strip() == test['html']:
        print(" > %s OK" % description)
    elif error:
        print(" > %s: ERROR" % description)
        print("   Exception: %s" % str(error))
    else:
        print(" > %s: FAIL" % description)
        print("   Expected: %s" % test['html'].replace('\n', '\\n'))
        print("   Actual  : %s" % html.replace('\n', '\\n'))


def run_all():
    with open('tests.json') as f:
        tests = json.load(f, object_pairs_hook=OrderedDict)
        for category, category_tests in tests.items():
            print(category)
            for description, test in category_tests.items():
                run_test(test, description)


run_all()
