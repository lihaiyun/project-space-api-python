from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from src.routes import user_routes
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
connect(host=app.config["MONGODB_URI"])

app.register_blueprint(user_routes.bp)

if __name__ == "__main__":
    app.run(debug=True)
