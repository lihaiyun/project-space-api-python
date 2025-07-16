from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from src.routes import user_routes, project_routes
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS with specific origins and credentials support
CORS(app, 
     origins=Config.CORS_ORIGINS,
     supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])

connect(host=app.config["MONGODB_URI"])

@app.route('/')
def hello():
    return {"message": "Hello! Welcome to the Project Space API"}

app.register_blueprint(user_routes.bp)
app.register_blueprint(project_routes.bp)

if __name__ == "__main__":
    app.run(debug=True)
