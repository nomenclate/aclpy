import pytest
import acls
from aclparse import acl


def test_name():
    #test setup
    with open('aristaacl.txt', 'r') as f:
        showacltest = f.read()

    result = acl.parseString(showacltest)

    parsedacl = acls.AccessList()
    parsedacl.name = result['name']

    for n in result['entry']:
        parsedacl.entries.append(n.asDict())

    name = 'THIS_IS_A_NAME'

    # Test results
    assert parsedacl.name == name
    assert result['name'] == name
    assert parsedacl.name == result['name']
    assert len(parsedacl.entries) == len(showacltest.splitlines())-2
