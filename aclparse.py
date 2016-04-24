import acls
import pyparsing as pp

def tokentoip(iptype):
    def parseAction(string, loc, tokens):
        if iptype == 'any':
            r = '0.0.0.0/0'
        if iptype == 'host':
            r = tokens[0] + '/32'
        return r
    return parseAction

pp.ParserElement.setDefaultWhitespaceChars(' \t')
lb, rb, dot, comma, slash = map(pp.Suppress, "[].,/")
host = pp.Literal('host')
lineno = pp.Word(pp.nums)
count = pp.Word(pp.nums)
action = pp.oneOf('permit deny')
portop = pp.oneOf('lt gt eq neq')
ports = pp.Word(pp.alphanums+'-')
protocol = pp.oneOf('ip tcp udp')
rangeop = pp.Literal('range')
ipoctet = pp.Word(pp.nums, max=3)
cidrmask = pp.Word(pp.nums, max=2)
ipaddr = pp.Combine(ipoctet + (dot + ipoctet) * 3, joinString='.')

name = pp.Combine((pp.Literal('IP Access List ').suppress()) +
                  pp.Word(pp.alphas+'_-')
                  )
hostip = (host.suppress() + ipaddr).setParseAction(tokentoip('host'))
net = pp.Combine(ipaddr +
                 slash +
                 cidrmask,
                 joinString='/')
anyip = pp.Literal('any').setParseAction(tokentoip('any'))
srcport = pp.OneOrMore(~(anyip ^ net ^ hostip) + ports)
dstport = pp.OneOrMore(ports)


counter = (lb +
           pp.Literal('match').suppress() +
           count('hits') +
           comma +
           pp.SkipTo(']')('delta') +
           rb
           )

condition = (protocol('protocol') +
            (anyip ^ hostip ^ net)('srcip') +
            ((pp.Optional(portop('srcop') + srcport('srcports'))) ^
             (pp.Optional(rangeop('srcop') + ports + ports))) +
            (anyip ^ hostip ^ net)('dstip') +
            ((pp.Optional(portop('dstop') + dstport('dstports'))) ^
             (pp.Optional(rangeop('dstop') + ports + ports)))
             )

aclentry = (lineno('index') +
            action('action') +
            condition('condition') +
            pp.Optional(counter('counter')) +
            pp.LineEnd().suppress()
            )('entry*')

acl = (name('name') + pp.LineEnd().suppress() +
       (pp.Literal('statistics per-entry') + pp.LineEnd()).suppress() +
       pp.OneOrMore(aclentry)
       )
