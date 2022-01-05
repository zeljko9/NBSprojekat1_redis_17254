import flask
from flask.wrappers import Request, Response
from flask_cors.decorator import cross_origin
from werkzeug.exceptions import HTTPException
import Baza as b
import threading
from flask import Flask, render_template
from flask_cors import CORS



app=Flask(__name__)
cors = CORS(app)
baza=b.Baza()
baza.resetuj()
print(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/PretplatiSe',methods=['POST'])
@cross_origin()
def pretplata():
    poruka=flask.request.json
    res=baza.pretplati_se((poruka['ime'], poruka['mejl']), list(poruka['zanrovi'].split(',')))
    print(poruka)

    response= app.response_class(
        response=flask.json.dumps(res),
        status=200
    )

    return response 

@app.route('/DePretplata',methods=['POST'])
@cross_origin()
def pretplata():
    poruka=flask.request.json
    baza.de_pretplata((poruka['mejl']))
    print(poruka)
    return flask.json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.errorhandler(HTTPException)
def handle_exception(e):
    print(e)

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()