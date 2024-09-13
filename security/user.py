import bcrypt
from database_conn.db_connection import DBConnection
from constants.constants import SCHEMA_NAME, USERS_TABLE


class User:
    @staticmethod
    def create_user(username, password, role):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = f"""
        INSERT INTO {SCHEMA_NAME}.{USERS_TABLE} (username, password, role)
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
        query = f"UPDATE {SCHEMA_NAME}.{USERS_TABLE} SET {', '.join(updates)} WHERE user_id = %s"
        try:
            DBConnection.execute_query(query, params)
            print("User updated successfully.")
        except Exception as e:
            print(f"Error updating user: {e}")

    @staticmethod
    def delete_user(userid):

        query = f"DELETE FROM {SCHEMA_NAME}.{USERS_TABLE} WHERE user_id = %s"
        try:
            DBConnection.execute_query(query, (userid,))
            print("User deleted successfully.")
        except Exception as e:
            print(f"Error deleting user: {e}")

    @staticmethod
    def authenticate_user(username, password):

        query = f"SELECT password FROM {SCHEMA_NAME}.{USERS_TABLE} WHERE username = %s"
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
        query = f"SELECT role FROM {SCHEMA_NAME}.{USERS_TABLE} WHERE username = %s"
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

        query = f"SELECT role FROM {SCHEMA_NAME}.{USERS_TABLE} WHERE username = %s"
        try:
            result = DBConnection.fetch_one(query, (username,))
            if result:
                user_role = result[0]
                return user_role == required_role
            return False
        except Exception as e:
            print(f"Error authorizing user: {e}")
            return False


