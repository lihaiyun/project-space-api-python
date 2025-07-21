from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image
import os
from src.config import Config
from src.utils.auth import token_required

bp = Blueprint("files", __name__, url_prefix="/files")

# Configure Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
    secure=True
)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_file_size(file):
    """Validate that the uploaded file doesn't exceed max size"""
    if hasattr(file, 'content_length') and file.content_length:
        return file.content_length <= Config.MAX_CONTENT_LENGTH
    
    # If content_length is not available, read and check size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset to beginning
    return size <= Config.MAX_CONTENT_LENGTH

def validate_image(file):
    """Validate that the uploaded file is a valid image"""
    try:
        image = Image.open(file)
        image.verify()
        file.seek(0)  # Reset file pointer after verification
        return True
    except Exception:
        return False

@bp.route("/upload", methods=["POST"])
@token_required
def upload_image(current_user):
    """
    Upload image to Cloudinary
    Requires authentication
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check file size
        if not validate_file_size(file):
            return jsonify({
                "error": f"File too large. Maximum size is {Config.MAX_CONTENT_IN_MB}MB"
            }), 413
        
        # Check file extension
        if not allowed_file(file.filename):
            allowed_types = ', '.join(Config.ALLOWED_EXTENSIONS)
            return jsonify({
                "error": f"Invalid file type. Allowed: {allowed_types}"
            }), 400
        
        # Validate image
        if not validate_image(file):
            return jsonify({"error": "Invalid image file"}), 400
        
        # Get optional parameters
        folder = request.form.get('folder', Config.UPLOAD_FOLDER)
        public_id = request.form.get('public_id')
        
        # Prepare upload options
        upload_options = {
            'folder': folder,
            'resource_type': 'image',
            'format': 'auto',
            'quality': 'auto:good',
            'fetch_format': 'auto',
            'transformation': [
                {'width': 1600, 'height': 900, 'crop': 'fill'},
                {'quality': 'auto:good'}
            ]
        }
        
        # Add public_id if provided
        if public_id:
            upload_options['public_id'] = f"{folder}/{secure_filename(public_id)}"
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(file, **upload_options)
        
        # Return success response
        return jsonify({
            "imageId": result['public_id'],
            "imageUrl": result['secure_url'],
            "createdAt": result['created_at']
        }), 201
        
    except Exception as err:
        return jsonify({"error": f"Upload failed: {str(err)}"}), 500

@bp.route("/info/<public_id>", methods=["GET"])
@token_required
def get_image_info(current_user, public_id):
    """
    Get image information from Cloudinary
    Requires authentication
    """
    try:
        # Replace URL encoding
        public_id = public_id.replace("%2F", "/")
        
        # Get resource info
        result = cloudinary.api.resource(public_id)
        
        return jsonify({
            "imageId": result['public_id'],
            "imageUrl": result['secure_url'],
            "format": result['format'],
            "width": result['width'],
            "height": result['height'],
            "bytes": result['bytes'],
            "createdAt": result['created_at'],
            "uploadedAt": result.get('uploaded_at', None)
        }), 200
        
    except Exception as err:
        return jsonify({"error": f"Failed to get image info: {str(err)}"}), 500

@bp.route("/delete/<public_id>", methods=["DELETE"])
@token_required
def delete_image(current_user, public_id):
    """
    Delete image from Cloudinary
    Requires authentication
    """
    try:
        # Replace URL encoding
        public_id = public_id.replace("%2F", "/")
        
        # Delete from Cloudinary
        result = cloudinary.uploader.destroy(public_id)
        
        if result['result'] == 'ok':
            return jsonify({
                "message": "Image deleted successfully",
                "public_id": public_id
            }), 200
        else:
            return jsonify({
                "error": "Failed to delete image",
                "result": result
            }), 400
            
    except Exception as err:
        return jsonify({"error": f"Delete failed: {str(err)}"}), 500

@bp.route("/config", methods=["GET"])
@token_required
def get_upload_config(current_user):
    """
    Get upload configuration limits and settings
    Requires authentication
    """
    try:
        return jsonify({
            "maxFileSize": Config.MAX_CONTENT_LENGTH,
            "maxFileSizeMB": Config.MAX_CONTENT_IN_MB,
            "allowedExtensions": list(Config.ALLOWED_EXTENSIONS),
            "defaultFolder": Config.UPLOAD_FOLDER,
            "supportedFormats": ["PNG", "JPG", "JPEG", "GIF", "WEBP"]
        }), 200
        
    except Exception as err:
        return jsonify({"error": f"Failed to get config: {str(err)}"}), 500
