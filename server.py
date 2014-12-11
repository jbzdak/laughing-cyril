# -*- coding: utf-8 -*-
import string

import random
import tornado
from tornado.ioloop import IOLoop
from tornado.httpserver import  HTTPServer
from tornado.process import fork_processes
from tornado.web import RequestHandler, Application, url
import hashlib
import sys, os
sys.path.append(os.path.dirname(__file__))

import loremipsum

class HelloHandler(RequestHandler):

    @tornado.web.authenticated
    def get(self):
        sha = hashlib.sha256()
        sha.update(self.request.path.encode('utf-8'))
        self.write("""
<html>
   <head>
      <title>Page with links </title>
   </head>
   <body>
        """)
        r = random.Random(int.from_bytes(sha.digest(), 'big'))
        g = loremipsum.Generator(random=r)
        for ii in range(r.randint(3, 10)):
            self.write("<p>")
            self.write(g.generate_paragraph()[2])
            link = "".join([r.choice(string.ascii_letters) for __ in range(10)])
            self.write(
                ' <a href="/{}"> {} </a> '.format(link, link)
            )
            self.write(g.generate_paragraph()[2])
        self.write(
            "</body></html>"
        )

    def get_current_user(self):
        if self.get_secure_cookie("logged_in") == b"true":
            return "user"

    def get_login_url(self):
        return "/login"


class Login(RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self, *args, **kwargs):
        username = self.get_argument("uname")
        password = self.get_argument("password")
        if username == "foo" and password == "bar":
            self.set_secure_cookie("logged_in", "true")
        self.redirect("/")

class Logout(RequestHandler):
    def get(self):
       self.clear_cookie("logged_in")
       self.redirect("/")

def make_app():
    return Application([
        url(r"/login", Login),
        url(r"/logout", Logout),
        url(r"/.*", HelloHandler)],
        cookie_secret="4") # Choosen by a fair dice roll

def main():
    app = make_app()
    server = HTTPServer(app)
    server.bind(4444)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

main()