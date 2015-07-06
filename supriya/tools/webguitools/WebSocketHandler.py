# -*- encoding: utf-8 -*-
import tornado.websocket


class WebSocketHandler(tornado.websocket.WebSocketHandler):

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