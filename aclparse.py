import acls
import pyparsing as pp

def portstodict(string, lok, tokens):
    if len(tokens) == 0:
        return None
    else:
        return {'portop':tokens[0],'port':tokens[1].asList()}

def tokentoip(iptype):
    def parseAction(string, loc, tokens):
        if iptype == 'any':
            r = '0.0.0.0/0'
        if iptype == 'host':
            r = tokens[0] + '/32'
        return r
    return parseAction

def checkcounter(string, lok, tokens):
    if len(tokens) == 0:
        print(tokens)
        return  {'hits': None, 'delta': None}

pp.ParserElement.setDefaultWhitespaceChars(' \t')
lb, rb, dot, comma, slash = map(pp.Suppress, "[].,/")
host = pp.Literal('host')
lineno = pp.Word(pp.nums)
count = pp.Word(pp.nums)
action = pp.oneOf('permit deny')
portop = pp.oneOf('lt gt eq neq range')
ports = pp.Word(pp.alphanums+'-')
protocol = pp.oneOf('ip tcp udp')
rangeop = pp.Literal('range')
ipoctet = pp.Word(pp.nums, max=3)
cidrmask = pp.Word(pp.nums, max=2)
ipaddr = pp.Combine(ipoctet + (dot + ipoctet) * 3, joinString='.')

name = pp.Combine((pp.Literal('IP Access List ').suppress()) +
                  pp.Word(pp.alphas+'_-'))

hostip = (host.suppress() + ipaddr).setParseAction(tokentoip('host'))
net = pp.Combine(ipaddr +
                 slash +
                 cidrmask,
                 joinString='/')

anyip = pp.Literal('any').setParseAction(tokentoip('any'))
srcport = portop + pp.Group(pp.OneOrMore(~(anyip ^ net ^ hostip) + ports))
dstports = portop + pp.Group(pp.OneOrMore(ports))

counter = (lb +
           pp.Literal('match').suppress() +
           count('hits') +
           comma +
           pp.SkipTo(']')('delta') +
           rb)

condition = (protocol('protocol') +
            (anyip ^ hostip ^ net)('srcip') +
            (pp.Optional((srcport)))('srcport').setParseAction(portstodict) +
            (anyip ^ hostip ^ net)('dstip') +
            (pp.Optional((dstports)))('dstport').setParseAction(portstodict))

aclentry = (lineno('index') +
            action('action') +
            condition('condition') +
            pp.Optional(counter('counter'), default=None) +
            pp.LineEnd().suppress())('entry*')

acl = (name('name') + pp.LineEnd().suppress() +
       (pp.Literal('statistics per-entry') +
       pp.LineEnd()).suppress() +
       pp.OneOrMore(aclentry))
