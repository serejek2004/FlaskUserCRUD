from datetime import datetime
from app import app, db
from flask import request, jsonify
from app.user.dto import UserDTO
from app.user.service import UserService

UserService = UserService(db)


@app.route('/user', methods=['POST'])
def register():
    """
    Register a new user.
    This endpoint registers a new user by providing user details.

    ---
    tags:
      - User
    parameters:
      - name: user
        in: body
        type: object
        required: true
        description: User information to be registered
        schema:
          type: object
          properties:
            username:
              type: string
              example: new_user
            email:
              type: string
              example: user@example.com
    responses:
      201:
        description: User successfully created
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                username:
                  type: string
                  example: new_user
                email:
                  type: string
                  example: user@example.com
      400:
        description: Invalid data provided
      409:
        description: Conflict - User already exists
    """
    data = request.get_json()
    user_dto = UserDTO.from_request(data)
    user, status_code = UserService.register(user_dto)

    return jsonify(user), status_code


@app.route('/user/<string:username>', methods=['GET'])
def get_users_by_username(username: str):
    """
    Get users by username.
    This endpoint retrieves users matching the given username.

    ---
    tags:
      - User
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: Username to search for
    responses:
      200:
        description: List of users with the given username
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              username:
                type: string
                example: username_example
              email:
                type: string
                example: user@example.com
      404:
        description: No users found
    """
    users = UserService.get_users_by_username(username)

    return jsonify(users), 200


@app.route('/user/email/<string:email>', methods=['GET'])
def get_user_by_email(email: str):
    """
    Get a user by email.
    This endpoint retrieves a user by the provided email.

    ---
    tags:
      - User
    parameters:
      - name: email
        in: path
        type: string
        required: true
        description: User email to retrieve
    responses:
      200:
        description: The user data
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            username:
              type: string
              example: user_example
            email:
              type: string
              example: user@example.com
      404:
        description: User not found
    """
    user = UserService.get_user_by_email(email)

    return jsonify(user), 200


def parse_datetime(date_str: str) -> datetime | None:
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


@app.route('/user/<string:start_datetime>/<string:end_datetime>')
def get_users_by_date_registration(start_datetime: str, end_datetime: str):
    """
    Get users by registration date range.
    This endpoint retrieves users who registered between the given dates.

    ---
    tags:
      - User
    parameters:
      - name: start_datetime
        in: path
        type: string
        required: true
        description: Start date in 'YYYY-MM-DDTHH:MM:SS' format
      - name: end_datetime
        in: path
        type: string
        required: true
        description: End date in 'YYYY-MM-DDTHH:MM:SS' format
    responses:
      200:
        description: List of users within the date range
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              username:
                type: string
                example: user_example
              email:
                type: string
                example: user@example.com
      400:
        description: Invalid date format
    """
    start_date = parse_datetime(start_datetime)
    end_date = parse_datetime(end_datetime)

    if start_date is None or end_date is None:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SS'"}), 400

    users = UserService.get_users_by_date_registration(start_date, end_date)
    return jsonify(users), 200


@app.route('/user/<string:username>/<string:start_datetime>/<string:end_datetime>')
def get_users_by_username_and_by_date_registration(username: str, start_datetime: datetime, end_datetime: datetime):
    """
    Get users by username and date of registration.
    This endpoint retrieves users matching the username and the given date range.

    ---
    tags:
      - User
    parameters:
      - name: username
        in: path
        type: string
        required: true
        description: Username to search for
      - name: start_datetime
        in: path
        type: string
        required: true
        description: Start date in 'YYYY-MM-DDTHH:MM:SS' format
      - name: end_datetime
        in: path
        type: string
        required: true
        description: End date in 'YYYY-MM-DDTHH:MM:SS' format
    responses:
      200:
        description: List of users matching the criteria
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              username:
                type: string
                example: user_example
              email:
                type: string
                example: user@example.com
      404:
        description: No users found with the given criteria
    """
    users = UserService.get_users_by_username_and_by_date_registration(username, start_datetime, end_datetime)

    return jsonify(users), 200


@app.route('/user', methods=['GET'])
def get_all():
    """
    Get all users.
    This endpoint retrieves all users in the system.

    ---
    tags:
      - User
    responses:
      200:
        description: List of all users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              username:
                type: string
                example: user_example
              email:
                type: string
                example: user@example.com
    """
    users = UserService.get_all()

    return jsonify(users), 200


@app.route('/user/<string:email>', methods=['DELETE'])
def delete_user_by_email(email: str):
    """
    Delete a user by email.
    This endpoint deletes a user using their email.

    ---
    tags:
      - User
    parameters:
      - name: email
        in: path
        type: string
        required: true
        description: Email of the user to delete
    responses:
      200:
        description: Successfully deleted the user
      404:
        description: User not found
    """
    is_deleted = UserService.delete_user_by_email(email)

    return 200 if is_deleted else 404


@app.route('/user/<string:email>', methods=['PUT'])
def update_user_by_email(email: str):
    """
    Update user by email.
    This endpoint updates a user's information by email.

    ---
    tags:
      - User
    parameters:
      - name: email
        in: path
        type: string
        required: true
        description: Email of the user to update
      - name: user
        in: body
        type: object
        required: true
        description: The updated user data
        schema:
          type: object
          properties:
            username:
              type: string
              example: new_user
            email:
              type: string
              example: new_user@example.com
    responses:
      200:
        description: Successfully updated the user
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            username:
              type: string
              example: new_user
            email:
              type: string
              example: new_user@example.com
      404:
        description: User not found
      409:
        description: Email already exists
    """
    data = request.get_json()
    user, status_code = UserService.update_user_by_email(email, UserDTO.from_request(data))

    return jsonify(user), status_code
