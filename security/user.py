import bcrypt
from database_conn.db_connection import DBConnection

class User:
    @staticmethod
    def create_user(username, password, role):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = """
        INSERT INTO shopdb.users (username, password, role)
        VALUES (%s, %s, %s);
        """
        params = (username, hashed_password.decode('utf-8'), role)
        try:
            DBConnection.execute_query(query, params)
        except Exception as e:
             print(f"Error creating user: {e}")


    @staticmethod
    def update_user(userid, username=None, password=None, role=None):
        updates = []
        params = []

        if username:
            updates.append("username = %s")
            params.append(username)
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            updates.append("password = %s")
            params.append(hashed_password.decode('utf-8'))
        if role:
            updates.append("role = %s")
            params.append(role)

        if not updates:
          return

        params.append(userid)
        query = f"UPDATE users SET {', '.join(updates)} WHERE userid = %s"
        try:
            DBConnection.execute_query(query, params)
        except Exception as e:
            print(f"Error updating user: {e}")

    @staticmethod
    def delete_user(userid):

        query = "DELETE FROM users WHERE userid = %s"
        try:
            DBConnection.execute_query(query, (userid,))
            print("User deleted successfully.")
        except Exception as e:
            print(f"Error deleting user: {e}")

    @staticmethod
    def authenticate_user(username, password):

        query = "SELECT password FROM shopdb.users WHERE username = %s"
        try:
            result = DBConnection.fetch_one(query, (username,))
            if result:
                hashed_password = result[0]
                # print(hashed_password,">>>>>>>>>>>>>>>>>>>>>>>",hashed_password.encode('utf-8'))
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            return False
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return False

    @staticmethod
    def get_role(username):
        query = "SELECT role FROM shopdb.users WHERE username = %s"
        try:
            result = DBConnection.fetch_one(query, (username,))
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"Error retrieving user role: {e}")
            return None

    @staticmethod
    def authorize_user(username, required_role):

        query = "SELECT role FROM shopdb.users WHERE username = %s"
        try:
            result = DBConnection.fetch_one(query, (username,))
            if result:
                user_role = result[0]
                return user_role == required_role
            return False
        except Exception as e:
            print(f"Error authorizing user: {e}")
            return False


if __name__ == "__main__":
    # Create a new user
    user_id = User.create_user('emp1', 'emp123', 'emp')
    print(f"User created with ID: {user_id}")

    # Authenticate user
    is_authenticated = User.authenticate_user('john_doe', 'securepassword')
    print(f"User authenticated: {is_authenticated}")

    # Authorize user
    is_authorized = User.authorize_user('john_doe', 'user')
    print(f"User authorized: {is_authorized}")

    User.update_user(user_id, password='newsecurepassword')

    User.delete_user(user_id)

    DBConnection.close()
