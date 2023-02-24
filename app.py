import flask
from api.index import main_route

app = flask.Flask(__name__)

app.register_blueprint(main_route)

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port='5001', debug=True)