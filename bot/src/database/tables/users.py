import sys
sys.path.append('../../') # src/

from database.main import execute, fetch

from datetime import datetime


class UsersTable:
    @staticmethod
    def addUser(user_id: int, timezone: str, created_at: datetime) -> None:
        stmt = '''
            INSERT INTO users (id, timezone, created_at)
            VALUES (%s, %s, %s)
        '''
        params = (user_id, timezone, created_at)

        execute(stmt, params)

    @staticmethod
    def getUser(user_id: int) -> dict:
        query = '''
            SELECT id, timezone, created_at
            FROM users
            WHERE id = %s
        '''
        params = (user_id, )
        
        user: dict = fetch(query, params, fetch_type='one', as_dict=True)
        
        return user
