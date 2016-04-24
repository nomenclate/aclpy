import aclparse as ap
with open('aristaacl.txt', 'r') as f:
      showacltest = f.read()

result = ap.acl.parseString(showacltest)

print(result['entry'][0]['condition'].asDict())
