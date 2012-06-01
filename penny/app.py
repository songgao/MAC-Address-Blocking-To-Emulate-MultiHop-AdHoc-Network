#!/usr/bin/python2.7

import tornado.ioloop
import tornado.web

from pachelbel import PachelbelHandler, PachelbelTextHandler, PachelbelJSONGeoAndTopo, PachelbelJSONInfo

if __name__ == "__main__":
    application = tornado.web.Application([
        (r'/pachelbelText', PachelbelTextHandler),
        (r'/pachelbel', PachelbelHandler),
        (r'/pachelbelJSONGeoAndTopo', PachelbelJSONGeoAndTopo),
        (r'/pachelbelJSONInfo', PachelbelJSONInfo),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ], debug=True)
    application.listen(9140)
    tornado.ioloop.IOLoop.instance().start()
