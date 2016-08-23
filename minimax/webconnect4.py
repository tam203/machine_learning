import SimpleHTTPServer
import SocketServer
import cgi
import re
from BaseHTTPServer import BaseHTTPRequestHandler

from minimax import min_max
from minimax.connect_4 import Connect4, RED_PLAYER, YELLOW_PLAYER


class Connect4Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        if None != re.search('/play', self.path):
            level = re.search(r'/play/([0-9]+)', self.path)
            depth = 4
            if level:
                depth = int(level.groups()[0])

            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type']})
            if "game" in form and "move" in form :
                #length = int(self.headers.getheader('content-length'))
                # data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                # recordID = self.path.split('/')[-1]
                # LocalData.records[recordID] = data
                game = Connect4(form.getvalue('game'))
                game.play(YELLOW_PLAYER, int(form.getvalue('move')))
                if game.get_winner() is YELLOW_PLAYER:
                    self.return_200_with_game("YOU WIN!!!")
                else:
                    game.play(RED_PLAYER, *min_max.pick_move(game, RED_PLAYER, max_depth=depth)[0])
                    if game.get_winner() is RED_PLAYER:
                        self.return_200_with_game("YOU LOSE!!!")
                    else:
                        self.return_200_with_game(game)
            else:
                self.send_response(400)
                self.end_headers()
        else:
            super(self.__class__, self).do_GET()


    def do_GET(self):
        if None != re.search('/play', self.path):
            if True:
                self.return_200_with_game(Connect4())
            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:
            super(self.__class__, self).do_GET()
        return

    def return_200_with_game(self, game):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(Con4View(game))


def Con4View(game):
    template = """
        <html>
            <head>
            <style>
                .r, .y {
                    display: inline-block;
                }
                .r {
                    background: red;
                }
                .y {
                    background: yellow
                }
                * {
                    font-family: monospace;
                }
            </style>
            </head>
            <body>
                <h1>You are YELLOW It's you're go</h1>
                %GAMEVIEW%
                <br/>
                <form method="POST" action="">
                    <label for="move">Col:</label>
                    <input id="move"  type="number" name="move" autofocus min="0" step="1" max="6"/>
                    <input id="game"  type="hidden" name="game" value="%GAME%"/>
                    <input type="submit" name="Play" value="Play" />
                </form>
                <a href="">Restart/play again</a>
            </body>
        </html>
    """
    gameview = ('|' + '|'.join((str(i) for i in xrange(7))) + '|\n' + str(game)).replace("\n","<br>")
    gameview = gameview.replace('Y','<span class="y">Y</span>')
    gameview= gameview.replace('R','<span class="r">R</span>')

    return template.replace("%GAMEVIEW%", gameview).replace('%GAME%', str(game))


PORT = 8000

httpd = SocketServer.TCPServer(("", PORT), Connect4Handler)

print "serving at port", PORT
httpd.serve_forever()