import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.escape import json_encode
import json
from tool import init_log, get_model, do_compress
from mod import get_client, do_get_cmd, do_post_cmd, do_task
from weirui import get_plan,get_module,get_psn,get_snstatus

def doTask():
    model = get_model()
    do_task(model)


def doCompress():
    do_compress()


class DoGet(tornado.web.RequestHandler):
    def post(self):
        model = get_model()
        client = get_client(model)
        ret = do_get_cmd(model, self.json_args["cmd"], client)
        print(ret)

    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None


class DoPut(tornado.web.RequestHandler):
    def post(self):
        model = get_model()
        client = get_client(model)
        ret = do_post_cmd(model, self.json_args["cmd"], client)

        self.write(json_encode(ret))

    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

class DoPost(tornado.web.RequestHandler):
    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
            rev1 = get_plan(self.json_args)
            self.write(rev1)
        else:
            self.json_args = {"Result":False,"Message":"json format error","Resultint":2000,"TaskID":"IF-46"}
            self.write(self.json_args)
        print(self.json_args)

class DoPost2(tornado.web.RequestHandler):
    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
            rev1 = get_module(self.json_args)
            self.write(rev1)
        else:
            self.json_args = {"Result":False,"Message":"json format error","Resultint":2000,"TaskID":"IF-50"}
            self.write(self.json_args)
        print(self.json_args)

class DoPost3(tornado.web.RequestHandler):
    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
            rev1 = get_psn(self.json_args)
            self.write(rev1)
        else:
            self.json_args = {"Result":False,"Message":"json format error","Resultint":2000,"TaskID":"IF-51"}
            self.write(self.json_args)
        print(self.json_args)

class DoPost4(tornado.web.RequestHandler):
    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
            rev1 = get_snstatus(self.json_args)
            self.write(rev1)
        else:
            self.json_args = {"Result":False,"Message":"json format error","Resultint":2000,"TaskID":"IF-48"}
            self.write(self.json_args)
        print(self.json_args)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("send success\n\r")
        self.write("send success\n\r")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/send", MainHandler),
        (r"/send/put", DoPut),
        (r"/send/get", DoGet),
        (r"/send/resvrve/sn",DoPost),
        (r"/send/resvrve/module", DoPost2),
        (r"/send/resvrve/psn", DoPost3),
        (r"/send/resvrve/status", DoPost4),
    ])


if __name__ == "__main__":
    init_log()

    app = make_app()
    app.listen(9900, "127.0.0.1")

    tornado.ioloop.PeriodicCallback(doTask, 1000 * 5).start()
    # tornado.ioloop.PeriodicCallback(doCompress, 1000 * 60 * 60 * 2).start()

    tornado.ioloop.IOLoop.current().start()


