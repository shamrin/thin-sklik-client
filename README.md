Thin Sklik Client
-----------------

Simple Python client for [Seznam Sklik API][1].  See test.py for usage and
http://api.sklik.cz for API documentation.

**Caution:** don't pass `session` argument to API methods. It gets passed
automatically (when needed).

### Why not official client?

There's an [official Sklik Python client][2]. But it's too complicated and
doesn't support all API methods. This library supports all methods because
it's just a thin [xmlrpclib][3] wrapper.

[1]: http://api.sklik.cz
[2]: http://github.com/seznam/sklik-api-python-client
[3]: http://docs.python.org/library/xmlrpclib.html 
