"""Seznam Sklik API"""

from pprint import pformat
from xmlrpclib import ServerProxy
from contextlib import contextmanager

def needs_session(methodname):
    """Return True when Sklik `methodname` needs session argument"""
    return not any(methodname.startswith(s)
                    for s in ('api.version', 'client.login', 'system.'))

def debug(*parts):
    print 'DEBUG', ' '.join(parts)

def dotted(s, limit=70, placeholder=' <...> '):
    n = (limit - len(placeholder)) // 2
    return s if len(s) <= limit else s[:n] + placeholder + s[-n:]

class SklikError(Exception):
    pass

class SklikProxy(ServerProxy):
    """Connection to Seznam Sklik XML-RPC sever (see http://api.sklik.cz)

    Mostly compatible with xmlrpclib.ServerProxy. Differences:
        * saves and passes `session` XML-RPC argument (when needed)
        * users shouldn't pass `session` argument manually
        * passes allow_none=True to ServerProxy
        * nice debug logging (optional)
    """

    def __init__(self, *args, **kw):
        """All unknown arguments are passed to xmlrpc.ServerProxy.__init__

        Specific to SklikProxy:
            loglevel - debug log level, 0 - no logging, 2 - full logging [0]
            exceptions - if True raise exceptions when status != 200 [False]
        """

        self.__session = None
        self.__debug = kw.pop('loglevel', 0)
        self.__exceptions = kw.pop('exceptions', False)

        kw.setdefault('allow_none', True)

        ServerProxy.__init__(self, *args, **kw)

    def _ServerProxy__request(self, methodname, params):
        if needs_session(methodname):
            assert self.__session is not None
            params = (self.__session,) + params

        if self.__debug: # log request
            p = params if not needs_session(methodname)\
                       else (dotted(params[0],30,'...'),) + params[1:]
            debug('OUT %s%r' % (methodname, p))

        res = ServerProxy._ServerProxy__request(self, methodname, params)

        if self.__debug: # log response
            format = pformat if self.__debug >= 2 else lambda d: dotted(str(d))

            if res.get('status') == 200:
                payload = dict((k, res[k]) for k in res if k not in
                                    ('status', 'statusMessage', 'session'))
                debug('IN', format(payload or res['statusMessage']))
            else:
                debug('IN', format(res))

        # save new session
        if 'session' in res and res['session'] != self.__session:
            if self.__debug:
                debug('session', 'renewed' if self.__session else 'created')
            self.__session = res['session']

        if self.__exceptions and 'status' in res and res['status'] != 200:
            if res['status'] in (400, 406):
                raise SklikError(res['statusMessage'], res['errors'])
            raise SklikError(res['status'], res['statusMessage'])

        return res


@contextmanager
def Client(url, login, password, *args, **kw):
    """Context manager that logs in on enter and logs out on exit

    Usage:
        >>> with Client(url, login, password, loglevel=1) as client:
        ...     client.listReports()
    """

    proxy = SklikProxy(url, *args, **kw)
    proxy.client.login(login, password)
    try:
        yield proxy
    finally:
        proxy.client.logout()

__all__ = ['SklikProxy', 'SklikError', 'Client']
