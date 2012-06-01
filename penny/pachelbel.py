import tornado.web
import tornado.template as template
import json

import __memcachedBridge as m

class PachelbelTextHandler(tornado.web.RequestHandler):
    def get(self):
        loader = template.Loader("templates")
        self.write(loader.load("pachelbelText.html").generate())

class PachelbelJSONGeoAndTopo(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(m.getGeoAndTopo()))

class PachelbelJSONInfo(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(m.getInfo()))

class PachelbelHandler(tornado.web.RequestHandler):
    def get(self):
        loader = template.Loader("templates")
        self.write(loader.load("pachelbel.html").generate())
