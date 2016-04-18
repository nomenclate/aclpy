import pytest
import acls
from aclparse import acl

with open('aristaacl.txt', 'r') as f:
    showacltest = f.read()

parsedacl = acls.AccessList()
result = acl.parseString(showacltest)
parsedacl.name = result['name']

for n in result['entry']:
    parsedacl.entries.append(n.asDict())

print(parsedacl.entries[98]['condition'])

def test_name():
    name = 'THIS_IS_A_NAME'
    assert parsedacl.name == name
    assert result['name'] == name
    assert parsedacl.name == result['name']
    assert len(parsedacl.entries) == 99
