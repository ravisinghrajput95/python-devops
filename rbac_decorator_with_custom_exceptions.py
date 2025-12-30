import functools

class AuthorizationError(Exception):
    """
    Raised when a user lacks the required role.
    """
    def __init__(self, user_name, required_role):
        self.user_name = user_name
        self.required_role = required_role
        message = f"User '{user_name}' lacks the required role: '{required_role}'."
        super().__init__(message)

def require_role(required_role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # Validation Step 1 (exact message expected by test)
            if 'user' not in kwargs:
                raise ValueError("A 'user' keyword argument is required")

            user = kwargs['user']

            if not isinstance(user, dict):
                raise ValueError("user must be a dictionary")

            if 'roles' not in user:
                raise ValueError("user dictionary must contain a 'roles' key")

            if not isinstance(user['roles'], list):
                raise ValueError("user['roles'] must be a list")

            user_name = user.get('name', 'unknown')

            if required_role not in user['roles']:
                raise AuthorizationError(user_name, required_role)

            return func(*args, **kwargs)

        return wrapper
    return decorator

@require_role("admin")
def delete_server(server_id, *, user):
    return f"Server {server_id} deleted"
admin_user = {
    "name": "alice",
    "roles": ["admin", "dev"]
}

try:
    result = delete_server("web01", user=admin_user)
    print(result)
except Exception as e:
    print(e)
