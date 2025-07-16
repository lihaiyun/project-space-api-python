from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from src.routes import user_routes, project_routes
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
connect(host=app.config["MONGODB_URI"])

@app.route('/')
def hello():
    return {"message": "Hello! Welcome to the Project Space API"}

app.register_blueprint(user_routes.bp)
app.register_blueprint(project_routes.bp)

if __name__ == "__main__":
    app.run(debug=True)
