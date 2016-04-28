import pytest
from acls import AccessList, Entry
from aclparse import acl


def test_name():
    #test setup
    with open('aristaacl.txt', 'r') as f:
        data = f.read()

    result = acl.parseString(data)

    parsedacl = AccessList(name=result['name'])

    parsedacl = AccessList(name=result['name'])
    for entry in result['entry']:
        parsedacl.entry(index=entry['index'],
                        action=entry['action'],
                        condition=entry['condition'],
                        counter=entry['counter'])

    name = 'THIS_IS_A_NAME'

    # Test results
    assert parsedacl.name == name
    assert result['name'] == name
    assert parsedacl.name == result['name']
    assert len(parsedacl) == len(data.splitlines())-2
