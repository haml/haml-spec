from __future__ import print_function, unicode_literals

import json
import regex

from collections import OrderedDict
from hamlpy import compiler


num_pass, num_fail, num_error = 0, 0, 0

DJANGO_VARIABLE_REGEX = regex.compile('{{([^}]+)}}')


def compile_haml(test):
    """
    Transform the given Haml into a Django template and perform variable substitution
    """
    dj_html = compiler.Compiler(options=test.get('config')).process(test['haml']).strip()

    def var_sub(match):
        return test.get('locals', {}).get(match.group(1).strip())

    # perform substitution of Django style {{ ... }} variable tags
    return DJANGO_VARIABLE_REGEX.sub(var_sub, dj_html)


with open('tests.json') as f:
    tests = json.load(f, object_pairs_hook=OrderedDict)
    for category, category_tests in tests.items():
        print(category)
        for description, test in category_tests.items():
            try:
                html = compile_haml(test)
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
