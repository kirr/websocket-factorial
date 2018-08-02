import math
import time

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

def factorial_with_timeout(n, timeout_sec):
    if n < 0:
        raise RuntimeError('n must be below zero')

    if n == 0:
        return 1

    res = 1
    start = time.time()
    for i in xrange(1, n+1):
        res *= i
        if i % 1000 == 0:
            if int(time.time() - start) > timeout_sec:
                raise RuntimeError('Timeout')
    return res


class FactorialService(WebSocket):

    def handleMessage(self):
        try:
            num = int(self.data)
            resp = unicode(factorial_with_timeout(num, 1))
        except Exception as e:
            resp = unicode(e)
        print self.address, 'message', resp
        self.sendMessage(resp)

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

server = SimpleWebSocketServer('', 8000, FactorialService)
server.serveforever()
