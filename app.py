from api import main_route
from flask_cors import CORS
from flask import Flask
from config import config
from util.core.limiter import limiter


app = Flask(__name__)

# Connect Config to app.config
app.config["SECRET_KEY"] = config["SECRET_KEY"]
app.config["JSON_AS_ASCII"] = False

limiter.init_app(app)

CORS(app)

app.register_blueprint(main_route)

@app.route("/")
def root():
    return "API Server is running"

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=config['PORT'], debug=config['FLASK_DEBUG'])