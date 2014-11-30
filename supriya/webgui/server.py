#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import supriya
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class SocketHandler(tornado.websocket.WebSocketHandler):

    def get_compression_options(self):
        return {}

    def open(self):
        self.application.watchers.add(self)
        print('OPENED')

    def on_close(self):
        self.application.watchers.remove(self)
        print('CLOSED')

    def on_message(self, message):
        pass

    def update(self, topic, event):
        try:
            event = event.copy()
            event['topic'] = topic
            self.write_message(event)
        except:
            pass


class WebServer(threading.Thread):

    ### INITIALIZER ###

    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
        self.server.subscription_service.subscribe(self, 'server-booted')
        self.server.subscription_service.subscribe(self, 'server-meters')
        self.server.subscription_service.subscribe(self, 'server-quit')
        self.server.subscription_service.subscribe(self, 'server-status')
        handlers = [
            (r'/', MainHandler),
            (r'/websocket', SocketHandler),
            ]
        self.application = tornado.web.Application(
            handlers,
            cookie_secret='MAGIC',
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            websocket_allow_origin='*',
            xsrf_cookies=True,
            )
        self.application.watchers = set()
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.daemon = True

    ### PUBLIC METHODS ###

    def notify(self, topic, event):
        for watcher in self.application.watchers:
            self.ioloop.add_callback(watcher.update, topic, event)

    def run(self):
        self.application.listen(8888)
        self.ioloop.start()


server = supriya.Server().boot()
web_server = WebServer(server)
web_server.start()
server.meters.allocate()