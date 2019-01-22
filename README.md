# ACLpy
Basic ACL parser that I wrote while learning python. It was a learning project inspired in part by [trigger](https://github.com/trigger/trigger), it is functional but unfinished.  The learning process was more important than finished product.

The idea was to create a parser using pyparsing that would parse ACLS from assorted vendors and store the parsed data into a vendor agnostic format.

Once in this vendor agnostic format the ACL could be maniuplated as needed, add/remove/edit entries, scanned for duplicate entries etc. Then wrtten back out in vendor specific output as needed.

Alot of the code was largely me exploring data structures and classes in python as a learning project, in that regard the project was a success even if not actually complete.

I used pyparsing primarily because it was less time consuming and more straight forward than implementing the parser via custom regex. The parsing was a means to an end the manipulation library was the meat of the work.

## Work that was completed

* The parser will parse most Cisco friendly formats.
* The manipulation library will handle most commom ACL contructs
* while the parser and output currently is cisco specific, the manipulation library understands concepts from other vendors.
