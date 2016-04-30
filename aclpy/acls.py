from ipaddress import IPv4Network
from collections import namedtuple

_counter = namedtuple('counter', ['hits', 'delta'])


class _Protocol(object):
    def __init__(self, protocols):
        if protocols is None:
            self._data = ['ip']
        else:
            if not isinstance(protocols, list):
                protocols = [protocols]
            self._data = [n for n in protocols]

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return repr(self._data)

    def contains(self, other):
        for item in other:
            if self._data == ['ip']:
                return True
            else:
                return any([(item in n) for n in self])


class _Port(object):
    portnames = {
        # TCP ports start here
        'acap': 674,  # Application Configuration Access Protocol
        'acr-nema': 104,  # ACR-NEMA Digital Imaging and Comms in Medicine
        'afpovertcp': 548,  # Apple Filing Protocol Over TCP
        'arns': 384,  # A Remote Network Server System
        'asip-webadmin': 311,  # AppleShare IP Web Administration
        'at-rtmp': 201,  # AppleTalk Routing Maintenance
        'aurp':  387,  # Appletalk Update-Based Routing Protocol
        'bftp': 152,  # Background File Transfer Program
        'bgmp': 264,  # Border Gateway Multicast Protocol
        'bgp': 179,  # Border Gateway Protocol
        'chargen': 19,  # Character Generator
        'cisco-tdp': 711,  # Cisco Tag Distribution Protocol
        'citadel': 504,  # Citadel
        'clearcase': 371,  # Clearcase albd
        'cmd': 514,  # Remote Shell/Rsh
        'commerce': 542,  # Commerce Applications
        'courier': 530,  # Remote Procedure Call
        'csnet-ns': 105,  # CCSO Name Server Protocol
        'daytime': 13,  # Daytime
        'dhcp-failover2': 847,  # DHCP Failover Protocol
        'dhcpv6-client': 546,  # DHCPv6 Client
        'dhcpv6-server': 547,  # DHCPv6 Server
        'discard': 9,  # Discard
        'domain': 53,  # Domain Name Service
        'dsp': 33,  # Display Support Protocol
        'echo': 7,  # Echo
        'efs': 520,  # Extended File Name Server
        'epp': 700,  # Extensible Provision Protocol
        'esro-gen': 259,  # Efficient Short Remote Operations
        'exec': 512,  # Remote Process Execution/Rexec
        'finger': 79,  # Finger
        'ftp': 21,  # File Transfer Protocol
        'ftp-data': 20,  # FTP data connections
        'ftps': 990,  # FTPS Protocol (control)
        'ftps-data': 989,  # FTPS Protocol (data)
        'godi': 848,  # Group Domain of Interpretation Protocol
        'gopher': 70,  # Gopher
        'gre': 47,  # Generic Routing Encapsulation
        'ha-cluster': 694,  # Linux-HA Heartbeat
        'hostname': 101,  # NIC hostname server
        'hp-alarm-mgr': 383,  # HP Performance Data Alarm Manager
        'http-alt': 591,  # Filemaker, Inc. -HTTP Alternate
        'http-mgmt': 280,  # http-mgmt
        'http-rpc-epmap': 593,  # HTTP RPC Ep Map
        'https': 443,  # HTTP Secure (HTTPS)
        'ident': 113,  # Ident Protocol
        'ieee-mms-ssl': 695,  # IEEE Media Management System Over SSL
        'imap': 143,  # Interim Mail Access Protocol
        'imap3': 220,  # Interactive Mail Access Protocol v3
        'imaps': 993,  # Internet Message Access Protocol over SSL
        'ipp':  631,  # Internet Printing Protocol
        'ipx': 213,  # Internetwork Packet Exchange
        'irc': 194,  # Internet Relay Chat
        'iris-beep': 702,  # Internet Registry Information Service Over BEEP
        'iscsi': 860,  # Internet Small Computers Systems Interface
        'isi-gl': 55,  # ISI Graphics Language
        'iso-tsap': 102,  # ISO-TSAP Class 0
        'kerberos': 88,  # Kerberos Authentication System
        'kerberos-adm': 749,  # Kerberos Administration
        'klogin': 543,  # Kerberos login
        'kpasswd': 464,  # Kerberos Change/Set Password
        'kshell': 544,  # Kerberos shell
        'la-maint': 51,  # IMP Logical Address Maintenance
        'lanz': 50001,  # Lanz Streaming
        'ldap': 389,  # Lightweight Directory Access Protocol
        'ldaps': 636,  # LDAP Over TLS/SSH
        'lmp': 701,  # Link Management Protocol
        'login': 513,  # Rlogin
        'lpd': 515,  # Line Printer Daemon
        'mac-srvr-admin': 660,  # MacOS Server Admin
        'matip-type-a':  350,  # MATIP Type A
        'matip-type-b': 351,  # MATIP Type B
        'microsoft-ds': 445,  # Microsoft-DS SMB File Sharing
        'mlag': 4432,  # MLAG Protocol
        'mpp': 218,  # Netix Message Posting Protocol
        'ms-sql-m': 1434,  # Microsoft SQL Monitor
        'ms-sql-s': 1433,  # Microsoft SQL Server
        'msdp': 639,  # Multicast Source Discovery Protocol
        'msexch-routing': 691,  # MS Exchange Routing
        'msg-icp': 29,  # MSG ICP
        'msp': 18,  # Message Send Protocol
        'nas': 991,  # Netnews Administration System
        'ncp': 524,  # NetWare Core Protocol
        'netrjs-1': 71,  # Remote Job Service
        'netrjs-2': 72,  # Remote Job Service
        'netrjs-3': 73,  # Remote Job Service
        'netrjs-4': 74,  # Remote Job Service
        'netwnews': 532,  # Readnews
        'new-rwho': 550,  # new-who
        'nfs': 2049,  # Network File System
        'nntp': 119,  # Network News Transport Protocol
        'nntps': 563,  # Network News Transfer Protocol Over TSL/SSH
        'nsw-fe': 27,  # NSW User System FE
        'odmr': 366,  # On Demand Mail Retry
        'openvpn': 1194,  # OpenVPN
        'pim-auto-rp': 496,  # PIM Auto-RP
        'pkix-timestamp': 318,  # PKIX Timestamp
        'pkt-krb-ipsec': 1293,  # Internet Protocol Security
        'pop2': 109,  # Post Office Protocol v2
        'pop3': 110,  # Post Office Protocol v3
        'pop3s': 995,  # Post Office Protocol 3 over TLS/SSL
        'pptp': 1723,  # Microsoft Point-to-Point Tunneling Protocol
        'print-srv': 170,  # Network PostScript
        'ptp-event': 319,  # Precision Time Protocol Event
        'ptp-general': 320,  # Precision Time Protocol General
        'qmtp': 209,  # The Quick Mail Transfer Protocol
        'qotd': 17,  # Quote of the Day
        'radius': 1812,  # Radius Authentication Protocol
        'radius-acct': 1813,  # Radius Accounting Protocol
        're-mail-ck': 50,  # Remote Mail Checking Protocol
        'remotefs': 556,  # RFS Server
        'repcmd': 641,  # SupportSoft Nexus Remote Command
        'rje': 5,  # Remote Job Entry
        'rlp': 39,  # Resource Location Protocol
        'rlzdbase': 635,  # RLZ DBase
        'rmc': 657,  # Remote Monitoring and Control Protocol
        'rpc2portmap': 369,  # Rpc2portmap
        'rsync': 873,  # rysnc File Synchronization Protocol
        'rtelnet': 107,  # Remote Telnet Service
        'rtsp': 554,  # Real Time Streaming Protocol
        'sgmp': 153,  # Simple Gateway Monitoring Protocol
        'silc': 706,  # Secure Internet Live Conferencing
        'smtp': 25,  # Simple Mail Transport Protocol
        'smux': 199,  # SNMP Unix Multiplexer
        'snagas': 108,  # SNA Gateway Access Server
        'snmp': 161,  # Simple Network Management Protocol
        'snmptrap': 162,  # SNMP Traps
        'snpp': 444,  # Simple Network Paging Protocol
        'sqlserv': 118,  # SQL Services
        'sqlsrv': 156,  # SQL Service
        'ssh': 22,  # Secure Shell Protocol
        'submission': 587,  # Email Message Submission
        'sunrpc': 111,  # Sun Remote Procedure Call
        'svrloc': 427,  # Server Location Protocol
        'systat': 11,  # Active users
        'tacacs': 49,  # TAC Access Control System
        'talk': 517,  # Talk
        'tbrpf': 712,  # Topology Broadcast based on RPF
        'tcpmux': 1,  # TCP Port Service Multiplexer
        'tcpnethaspsrv': 475,  # Aladdin Knowledge Systems Hasp services
        'telnet': 23,  # Telnet Protocol
        'time': 37,  # Time
        'tunnel': 604,  # TUNNEL Profile
        'ups': 401,  # Uninterruptible Power Supply
        'uucp': 540,  # Unix-to-Unix Copy Program
        'uucp-path': 117,  # UUCP Path Service
        'vmnet': 175,  # VMNET
        'whois': 43,  # Nicname
        'www': 80,  # World Wide Web (HTTP)
        'xns-ch': 54,  # XNS (Xerox Network Systems) Clearinghouse
        'xns-mail': 58,  # XNS (Xerox Network Systems) Mail
        'xns-time': 52,  # XNS (Xerox Network Systems) Time Protocol
        'z39-50': 210,  # ANSI Z39.50
        # UDP ports start here
        'asf-rmcp': 623,  # ASF Remote Management and Control Protocol
        'auth': 113,  # Authentication Service
        'bfd': 3784,  # Bidirectional Forwarding Detection
        'bfd-echo': 3785,  # BFD Echo
        'biff': 512,  # Biff (mail notification, comsat)
        'bootpc': 68,  # Bootstrap Protocol (BOOTP) client
        'bootps': 67,  # Bootstrap Protocol (BOOTP) server
        'dnsix': 195,  # DNSIX security protocol auditing
        'gtp-c': 2123,  # GPRS Tunneling Protocol Control Data
        'gtp-prime': 3386,  # GPRS Tunneling Prime Protocol
        'gtp-u': 2152,  # GPRS Tunneling Protocol User Data
        'isakmp': 500,  # ISAKMP
        'l2tp': 1701,  # Layer 2 Tunneling Protocol
        'mobile-ip': 434,  # Mobile IP registration
        'monitor': 561,  # Monitord
        'nameserver': 42,  # IEN116 Nameserver Service (obsolete)
        'netbios-dgm': 138,  # NetBios datagram service
        'netbios-ns': 137,  # NetBios name service
        'netbios-ss': 139,  # NetBios session service
        'netwall': 533,  # For Emergency Broadcasts
        'non500-isakmp': 4500,  # ISAKMP
        'ntp': 123,  # Network Time Protocol
        'olsr': 698,  # Optimized Link State Routing
        'rip': 520,  # Routing Information Protocol
        'rmonitor': 560,  # Remote Monitord
        'syslog': 514,  # System Logger
        'tftp': 69,  # Trivial File Transfer Protocol
        'timed': 525,  # Timeserver
        'who': 513,  # Who service, rwho
        'xdmcp': 177,  # X Display Manager Control Protocol
    }

    def __init__(self, ports):
        if ports is None:
            self._data = []
        else:
            self._data = []
            for port in ports:
                port['port'] = [_Port.name_to_port(n) for n in port['port']]
                self._data.append(port)

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return repr(self._data)

    @classmethod
    def name_to_port(cls, name):
        if name in cls.portnames.keys():
            return cls.portnames[name]
        else:
            return int(name)

    # TODO: This Needs to be cleaned up
    def contains(self, other):
        for otherportobj in [entry for entry in other]:
            for otherport in otherportobj['port']:
                for myportobj in self:
                    myport = myportobj['port']
                    myportop = myportobj['portop']
                    if myportop == 'eq':
                        return any([otherport == n for n in myport])
                    elif myportop == 'range':
                        return myport[0] <= otherport <= myport[1]
                    elif myportop == 'gt':
                        return otherport > myport[0]
                    elif myportop == 'lt':
                        return otherport > myport[0]
                    elif myportop == 'neq':
                        return otherport != myport[0]


class _Address(object):
    def __init__(self, addresses):
        if addresses is None:
            self._data = [IPv4Network('0.0.0.0/0')]
        else:
            self._data = [self.string_to_ip(n) for n in addresses]

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return repr(self._data)

    @staticmethod
    def string_to_ip(ipaddress):
        """Converts ip address passed as a string to an IPv4Network

        Args:
            ipaddress(str): an IP address as a string either as a host
            address (i.e. 10.0.0.0) or as a CIDR network (i.e. 10.0.0.0/8)

        Returns:
            IPv4Network(object)"""
        if '/' in ipaddress:
            return IPv4Network(ipaddress)
        else:
            return IPv4Network(ipaddress+'/32')

    def contains(self, matchip):
        """Comapares two isntances of _Address class to determine if they
            overlap"""
        for item in matchip:
            if isinstance(item, IPv4Network):
                return any([address.overlaps(item) for address in self])
            else:
                raise TypeError('{} is not IPv4Network'.format)


class Condition(object):
    """Container class for condition objects"""
    conditions = {'protocol': _Protocol,
                  'srcip': _Address,
                  'dstip': _Address,
                  'srcport': _Port,
                  'dstport': _Port}

    def __init__(self):
        self.__data = {}

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, key):
        return self.__data[key]

    def __delitem__(self, key):
        del self.__data[key]

    def __iter__(self):
        return iter(self.__data.items())

    def __repr__(self):
        return repr(self.__data)

    def contains(self, other):
        return all([self[k].contains(other[k]) for k, v in self])

    @classmethod
    def condition(cls, **kwargs):
        condition = Condition()
        for key, value in kwargs.items():
            if key in cls.conditions.keys():
                if not isinstance(value, list):
                    value = [value]
                condition[key] = cls.conditions[key](value)
        return condition


class Entry(object):
    """An Entry in an AccessList"""

    # pylint: disable=too-many-arguments
    # I'm cool with this
    validkeys = {'name': str,
                 'index': int,
                 'action': str,
                 'condition': Condition,
                 'counter': _counter}

    def __init__(self,
                 name=None,
                 index=None,
                 action=None,
                 condition=None,
                 counter=None):

        self.__data = {}
        if name is not None:
            self.name = name
        if index is not None:
            self.index = int(index)
        if action is None:
            self.action = 'permit'
        else:
            self.action = action
        self.condition = Condition.condition(**condition)
        if counter is not None:
            self['counter'] = _counter(counter['hits'], counter['delta'])

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        if key in Entry.validkeys and isinstance(value, Entry.validkeys[key]):
            self.__data[key] = value
        else:
            raise TypeError('{} is wrong type')

    def __delitem__(self, key):
        del self.__data[key]

    def __iter__(self):
        return iter(self.__data)

    def __repr__(self):
        return repr(self.__data)

    @property
    def name(self):
        """Get name of Condition"""
        return self['name']

    @name.setter
    def name(self, value):
        self['name'] = value

    @property
    def index(self):
        """Get index of Condition"""
        return self['index']

    @index.setter
    def index(self, value):
        self['index'] = value

    @property
    def action(self):
        """Get action"""
        return self['action']

    @action.setter
    def action(self, value):
        self['action'] = value

    @property
    def condition(self):
        """Get condition"""
        return self['condition']

    @condition.setter
    def condition(self, condition):
        self['condition'] = condition

    @property
    def hits(self):
        """Get hits"""
        if self['counter']:
            return self['counter']['hits']
        else:
            return None

    @property
    def delta(self):
        """Get delta"""
        if self['counter']:
            return self['counter']['delta']
        else:
            return None


class AccessList(object):
    """a List like object for interacting with access lists
    Attributes:
        name (str): A string that functions as the name of the access lists.
            Used as the name when outputing named access-lists """

    def __init__(self, name=None):
        self.__entries = []
        self._name = None
        self.name = name

    def __len__(self):
        return len(self.__entries)

    def __getitem__(self, key):
        return self.__entries[key]

    def __setitem__(self, key, value):
        if isinstance(value, Entry):
            self.__entries[key] = value
        else:
            raise TypeError('value is {} and not {}'.format(type(value),
                                                            Entry))

    def __delitem__(self, key):
        del self.__entries[key]

    def __iter__(self):
        return iter(self.__entries)

    def ismatch(self, match):
        for entry in self:
            if entry.condition.contains(match):
                return True
        return False

    def output(self):
        """Placeholder for output method"""
        pass

    def append_entry(self, **kwargs):
        self.append(Entry(**kwargs))

    def append(self, entry):
        """Appends Entry object to AccessList"""
        if isinstance(entry, Entry):
            self.__entries.append(entry)
        else:
            raise TypeError('{} is not a supported type'.format(type(entry)))

    def insert_entry(self, key, entry):
        """Inserts an Entry object after the entry indicated by key"""
        if isinstance(entry, Entry):
            self.__entries.insert(self, key, entry)
        else:
            raise TypeError('{} is not a supported type'.format(type(entry)))

    def resequence(self, step=1):
        """Resequences line numbers of accesslist incrementing by step
            value
        Args:
            step (Optional[int]): the value to increment by. Defaults to 1
        Raises:
            ValueError: If step is less than or equal to zero
        """
        if step <= 0:
            raise ValueError('step must be positive non zero value')

        for entry, newindex in zip(self, range(step, len(self)*step*2, step)):
            entry.index = newindex

    @property
    def name(self):
        """Name of access list"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
