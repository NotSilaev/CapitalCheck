import sys
sys.path.append('../../') # src/

from database.main import execute, fetch

import uuid
import datetime


class OrdersTable:
    @staticmethod
    def addOrder(user_id: int, asset: str, action: str, quantity: float, price: float) -> None:
        order_id = str(uuid.uuid4())
        created_at = datetime.datetime.now()

        stmt = '''
            INSERT INTO orders (id, user_id, asset, action, quantity, price, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        params = (order_id, user_id, asset, action, quantity, price, created_at)

        execute(stmt, params)
