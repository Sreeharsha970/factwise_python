import datetime


class UserBase:
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        from datetime import datetime

class UserManager:
    def _init_(self):
        self.users = {}  # Placeholder for storing users

    def create_user(self, request: str) -> str:
        import json

        try:
            data = json.loads(request)
            user_name = data.get('name')
            display_name = data.get('display_name')

            # Check constraints
            if not user_name or len(user_name) > 64:
                return '{"error": "Invalid user name"}'
            if len(display_name) > 64:
                return '{"error": "Display name exceeds maximum length"}'

            # Check if user name already exists
            if user_name in self.users:
                return '{"error": "User name already exists"}'

            # Generate user ID (for demonstration, it could be more sophisticated)
            user_id = str(len(self.users) + 1)

            # Store user data
            self.users[user_name] = {
                'id': user_id,
                'name': user_name,
                'display_name': display_name,
                'creation_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'description': ''  # Initialize with empty description
            }

            # Return response JSON
            return json.dumps({'id': user_id})

        except json.JSONDecodeError:
            return '{"error": "Invalid JSON format"}'

    def describe_user(self, request: str) -> str:
        import json

        try:
            data = json.loads(request)
            user_id = data.get('id')

            if user_id in self.users:
                user_data = self.users[user_id]
                response = {
                    'name': user_data['name'],
                    'description': user_data.get('description', ''),
                    'creation_time': user_data['creation_time']
                }
                return json.dumps(response)
            else:
                return '{"error": "User not found"}'

        except json.JSONDecodeError:
            return{"error":"Invalid JSON format"}
    # list all users
    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        pass

    # update user
    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        pass

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

