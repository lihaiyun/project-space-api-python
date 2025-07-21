from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from src.routes import user_routes, project_routes, file_route
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Set max content length for file uploads
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

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
app.register_blueprint(file_route.bp)

if __name__ == "__main__":
    # This is only for development - use Gunicorn for production
    print("Running in development mode...")
    print("For production, use: gunicorn -c gunicorn.conf.py src.app:app")
    app.run(debug=True, port=5000)
