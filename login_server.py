# -*- coding: utf-8 -*-
import hashlib

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url



def main():
    app = make_app()
    app.listen(4444)
    IOLoop.current().start()

main()