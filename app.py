from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from cgi import FieldStorage


# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()

routes = []


def route(path, method):
    routes.append((path, method))


# add route setting
route('/', 'index')
route('/index', 'index')

# data.
data = [['それは人間のペットですか', 1, 2],
        ['それはにゃーと鳴きますか', 'ネコ', 'イヌ'],
        ['それは食べると美味しいですか', 'うし', 'ライオン']
        ]


class HelloServerHandler(BaseHTTPRequestHandler):

    # GET method.
    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if (r[0] == _url.path):
                eval('self.' + r[1] + '()')
                break
        else:
            self.error()
        return

    # index action
    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Animal',
            last=-1,
            animal='',
            yes=0,
            no=0,
            message='質問に答えてね')
        self.wfile.write(html.encode('utf-8'))
        return

    # error action
    def error(self):
        global routes
        self.send_error(404, "cannnot access!!")
        return

    # post action
    def do_POST(self):
        _url = urlparse(self.path)
        if (_url.path == '/'):
            self.quiz()
        elif (_url.path == '/end'):
            self.end()
        return

    # next action
    def quiz(self):
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})
        try:
            answer = int(form['answer'].value)
            if (answer == -1):
                html = index.format(
                    title='Animal',
                    message='やった〜',
                    last=-1,
                    animal='',
                    yes=0,
                    no=0,
                )
            elif (answer == -2):
                html = next.format(
                    title='Animal',
                    message='うーん、答えを教えて',
                    last=form['last'].value,
                    animal=form['animal'].value
                )
            else:
                html = index.format(
                    title='Animal',
                    message=data[answer][0],
                    last=answer,
                    animal=form['answer'].value,
                    yes=data[answer][1],
                    no=data[answer][2])
        except:
            html = index.format(
                title='Animal',
                message='それは、　' + form['answer'].value + 'ですか。',
                last=form['last'].value,
                animal=form['answer'].value,
                yes=-1,
                no=-2
            )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        return

    # end action
    def end(self):
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})
        animalname = form['animalname'].value
        question = form['question'].value
        last = int(form['last'].value)
        animal = form['animal'].value
        newdata = [question, animalname, animal]
        n = len(data)
        if (data[last][1] == animal):
            data[last][1] = n
        elif (data[last][2] == animal):
            data[last][2] = n

        data.append(newdata)

        html = index.format(
            title='Animal',
            message='なるほど、分かりました',
            last=-1,
            animal='',
            yes=0,
            no=0,
        )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()
