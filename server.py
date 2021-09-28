import email
import io
from io import BytesIO
import mimetypes
import os
import posixpath
import shutil
import urllib
import datetime
import html
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler
import sys

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        super().__init__(*args, **kwargs)

    def calcScore(self, user_id, win):
        file = open("score.txt", "r")
        ids = []
        scores = []
        i = 0
        for line in file:
            tmp = line.split(" ")
            scores.append(tmp[0])
            ids.append(tmp[1])
            i+=1
        file.close()
        if (str(user_id) in str(ids[0])) and win:
            scores[0] = int(scores[0])
            scores[0] += 1
        elif (str(user_id) in str(ids[1])) and win:
            scores[1] = int(scores[1])
            scores[1] += 1
        elif (str(user_id) in str(ids[0])) and not win:
            scores[1] = int(scores[1])
            scores[1] += 1
        elif (str(user_id) in str(ids[1])) and not win:
            scores[0] = int(scores[0])
            scores[0] += 1
        os.remove("score.txt")
        file = open("score.txt", "w")
        file.write(str(scores[0]) + " " + str(ids[0]))
        file.write(str(scores[1]) + " " + str(ids[1]))
        file.close()



    def findWinner(self, user_id):
        f = open("play.txt", "r")
        p1 = []
        p2 = []
        for line in f:
            arr = line.split(" ")
            if not p1:
                p1 = arr
            else:
                p2 = arr
        win = False
        if "R" in p1:
            if "P" in p2:
                win = False
            elif "S" in p2:
                win = True
        elif "P" in p1:
            if "S" in p2:
                win = False
            elif "R" in p2:
                win = True
        elif "S" in p1:
            if "R" in p2:
                win = False
            elif "P" in p2:
                win = True
        if (user_id == int(p1[1])):
            if win:
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(b'You won this round!')
                self.calcScore(user_id, True)
            else:
                self.send_response(HTTPStatus.CONFLICT)
                self.end_headers()
                self.wfile.write(b'You lost!')
                self.calcScore(user_id, False)
        else:
            if win:
                self.send_response(HTTPStatus.CONFLICT)
                self.end_headers()
                self.wfile.write(b'You lost!')
                self.calcScore(user_id, False)
            else:
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(b'You won this round!')
                self.calcScore(user_id, True)

    def do_GET(self):
        print(self.client_address)
        print(self.path)


        arr = self.path.split('/')
        i = str(arr[2])
        user_id = int(arr[1])
        if i == "result":
            if not os.path.exists("play.txt"):
                self.send_response(HTTPStatus.CONFLICT)
                self.end_headers()   
                self.wfile.write(b'File not found')
                return
            elif len(open("play.txt").readlines()) < 2:
                self.send_response(HTTPStatus.CONFLICT)
                self.end_headers()   
                self.wfile.write(b'Finish the game first!')
                return
        f = open("play.txt", "r")
        p1 = []
        p2 = []
        for line in f:
            arr = line.split(" ")
            if not p1:
                p1 = arr
            else:
                p2 = arr
        win = False
        if "R" in p1:
            if "P" in p2:
                win = False
            elif "S" in p2:
                win = True
        elif "P" in p1:
            if "S" in p2:
                win = False
            elif "R" in p2:
                win = True
        elif "S" in p1:
            if "R" in p2:
                win = False
            elif "P" in p2:
                win = True
        if (user_id == int(p1[1])):
            if win:
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(b'You won this round!')
            else:
                self.send_response(HTTPStatus.CONFLICT)
                self.end_headers()
                self.wfile.write(b'You lost!')
        else:
            if win:
                self.send_response(HTTPStatus.CONFLICT)
                self.end_headers()
                self.wfile.write(b'You lost!')
            else:
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(b'You won this round!')

    def do_POST(self):
        arr = self.path.split('/')
        f = str(arr[2])
        user_id = int(arr[1])
        if(f == "R" or f == "P" or f == "S"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            if not os.path.exists("play.txt"):
                open('play.txt', 'w')
            if(len(open("play.txt").readlines()) >= 2):
                os.remove("play.txt")
                open('play.txt', 'w')
            if(len(open("play.txt").readlines()) == 1):
                file = open("play.txt", "r")
                i = file.readline()
                if(f in i):
                    content_length = int(self.headers['Content-Length'])
                    body = self.rfile.read(content_length)
                    self.send_response(HTTPStatus.CONFLICT)
                    self.end_headers()   
                    response = BytesIO()
                    response.write(b'Try again, both plays were identical')
                    response.write(body)
                    self.wfile.write(response.getvalue())
                    os.remove("play.txt")
                    if not os.path.exists("score.txt"):
                        file = open('score.txt', 'w')
                        file.close()
                    with open('score.txt') as p:
                        if not str(user_id) in p.read():
                            file = open("score.txt", "a")
                            file.write(str(0) + " " + str(user_id) + "\n")
                            file.close()
                    if (len(open("play.txt").readlines()) == 2):
                        self.findWinner(user_id)
                    return
                if(str(user_id) in i):
                    content_length = int(self.headers['Content-Length'])
                    body = self.rfile.read(content_length)
                    self.send_response(HTTPStatus.CONFLICT)
                    self.end_headers()   
                    response = BytesIO()
                    response.write(b'Waiting for opponent')
                    response.write(body)
                    self.wfile.write(response.getvalue())
                    os.remove("play.txt")
                    if not os.path.exists("score.txt"):
                        file = open('score.txt', 'w')
                        file.close()
                    with open('score.txt') as p:
                        if not str(user_id) in p.read():
                            file = open("score.txt", "a")
                            file.write(str(0) + " " + str(user_id) + "\n")
                            file.close()
                    if (len(open("play.txt").readlines()) == 2):
                        self.findWinner(user_id)
                    return

            self.send_response(HTTPStatus.OK)
            self.end_headers()
            response = BytesIO()
            response.write(b'Accepted')
            response.write(body)
            self.wfile.write(response.getvalue())
            file = open("play.txt", "a")
            file.write(f + " " + str(user_id) +"\n")
            file.close()
            if not os.path.exists("score.txt"):
                file = open('score.txt', 'w')
                file.close()
            with open('score.txt') as p:
                if not str(user_id) in p.read():
                    file = open("score.txt", "a")
                    file.write(str(0) + " " + str(user_id) + "\n")
                    file.close()
            if (len(open("play.txt").readlines()) == 2):
                self.findWinner(user_id)
        elif(f == "reset"):
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            if not os.path.exists("reset.txt"):
                open('reset.txt', 'w')
            with open('reset.txt') as p:
                if not str(user_id) in p.read():
                    file = open("reset.txt", "a")
                    file.write(f + " " + str(user_id) +"\n")
                    file.close()
            

            if((len(open("reset.txt").readlines()) == 2)) :
                os.remove("play.txt")
                open("play.txt", "w")
                os.remove("reset.txt")
                open("reset.txt", "w")
                os.remove("score.txt")
                open("score.txt", "w")
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                response = BytesIO()
                response.write(b'**Game reset**')
                response.write(body)
                self.wfile.write(response.getvalue())
                return

            self.send_response(HTTPStatus.OK)
            self.end_headers()
            response = BytesIO()
            response.write(b'Waiting on opponent')
            response.write(body)
            self.wfile.write(response.getvalue())


        elif (f == "score"):
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            self.send_response(HTTPStatus.OK)
            self.end_headers()
            response = BytesIO()
            file = open("score.txt", "r")
            for line in file:
                response.write(str.encode(line))
            response.write(body)
            self.wfile.write(response.getvalue())

        

        
            

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', int(sys.argv[1]))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run(HTTPServer, MyHTTPRequestHandler)

