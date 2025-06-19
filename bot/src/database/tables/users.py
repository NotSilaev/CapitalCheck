import sys
sys.path.append('../../') # src/

from database.main import execute, fetch

import datetime


class UsersTable:
    @staticmethod
    def addUser(user_id: int) -> None:
        created_at = datetime.datetime.now()

        stmt = '''
            INSERT INTO users (id, created_at)
            VALUES (%s, %s)
        '''
        params = (user_id, created_at)

        execute(stmt, params)

    @staticmethod
    def getUser(user_id: int) -> dict:
        query = '''
            SELECT id, created_at
            FROM users
            WHERE id = %s
        '''
        params = (user_id, )
        
        user: dict = fetch(query, params, fetch_type='one', as_dict=True)

        return user
