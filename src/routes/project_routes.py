from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.models.project import Project
from src.schemas.project_schema import ProjectSchema, ProjectInputSchema
from src.utils.auth import token_required

bp = Blueprint("projects", __name__, url_prefix="/projects")

# Schema instances
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
input_schema = ProjectInputSchema()

@bp.route("/", methods=["GET"])
def list_projects():
    """
    Get all projects with optional search and sorting
    Query parameters:
    - search: Search projects by name or description (case-insensitive)
    - limit: Limit number of results (default: 50)
    - skip: Skip number of results for pagination (default: 0)
    - sort: Sort by field (default: dueDate)
    - order: Sort order - 'asc' or 'desc' (default: asc)
    """
    try:
        # Get query parameters
        search_query = request.args.get('search', '').strip()
        limit = min(int(request.args.get('limit', 50)), 100)  # Max 100 results
        skip = int(request.args.get('skip', 0))
        sort_field = request.args.get('sort', 'dueDate')
        sort_order = request.args.get('order', 'asc').lower()
        
        # Validate sort parameters
        allowed_sort_fields = ['dueDate', 'createdAt', 'updatedAt', 'name', 'status']
        if sort_field not in allowed_sort_fields:
            sort_field = 'dueDate'
        
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'
        
        # Build the query
        query = {}
        
        if search_query:
            # Case-insensitive search in name and description
            query = {
                '$or': [
                    {'name': {'$regex': search_query, '$options': 'i'}},
                    {'description': {'$regex': search_query, '$options': 'i'}}
                ]
            }
        
        # Execute query with pagination and sorting
        sort_prefix = '+' if sort_order == 'asc' else '-'
        sort_string = f"{sort_prefix}{sort_field}"
        
        projects = Project.objects(__raw__=query).order_by(sort_string).skip(skip).limit(limit)
        total_count = Project.objects(__raw__=query).count()
        
        # Prepare response
        response_data = {
            "projects": projects_schema.dump(projects),
            "pagination": {
                "total": total_count,
                "limit": limit,
                "skip": skip,
                "hasMore": (skip + limit) < total_count
            },
            "sorting": {
                "field": sort_field,
                "order": sort_order
            }
        }
        
        if search_query:
            response_data["search"] = search_query
        
        return jsonify(response_data), 200
        
    except ValueError as err:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@bp.route("/", methods=["POST"])
@token_required
def create_project(current_user):
    """
    Create a new project
    Requires authentication
    """
    try:
        # Validate input data
        data = input_schema.load(request.get_json())
        
        # Handle owner assignment
        print(current_user)
        data['owner'] = current_user.id
        
        # Create project
        project = Project(**data)
        project.save()
        
        return jsonify(project_schema.dump(project)), 201
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@bp.route("/<project_id>", methods=["GET"])
def get_project(project_id):
    """
    Get a specific project by ID
    """
    try:
        project = Project.objects(id=project_id).first()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        return jsonify(project_schema.dump(project)), 200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@bp.route("/<project_id>", methods=["PUT"])
@token_required
def update_project(current_user, project_id):
    """
    Update a project (full update)
    Requires authentication
    """
    try:
        # Find project
        project = Project.objects(id=project_id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Check owner permission
        if project.owner and str(project.owner.id) != str(current_user.id):
            return jsonify({"error": "You do not have permission to update this project"}), 403

        # Validate input data
        data = input_schema.load(request.get_json())
        
        # Update all provided fields
        for field, value in data.items():
            if hasattr(project, field):
                setattr(project, field, value)
        
        project.save()
        
        return jsonify(project_schema.dump(project)), 200
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@bp.route("/<project_id>", methods=["DELETE"])
@token_required
def delete_project(current_user, project_id):
    """
    Delete a project
    Requires authentication
    """
    try:
        # Find project
        project = Project.objects(id=project_id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Check owner permission
        if project.owner and str(project.owner.id) != str(current_user.id):
            return jsonify({"error": "You do not have permission to delete this project"}), 403

        # Delete project
        project.delete()
        
        return jsonify({"message": "Project deleted successfully"}), 200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500
