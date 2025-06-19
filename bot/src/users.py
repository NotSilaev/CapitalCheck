from database.tables.users import UsersTable
from cache import setCacheValue, getCacheValue

from aiogram.types.user import User


def doesUserExist(user_id: int) -> bool:
    "Checks if the user exists in the cache and in the database."

    user_cache = getCacheValue(f'user-{user_id}')
    if user_cache:
        return True

    user = UsersTable.getUser(user_id)
    if user:
        setCacheValue(key=f'user-{user_id}', value='exists')
        return True

    return False


def addUser(user_id: int) -> None:
    "Adds the user to the database and saves the data to the cache."

    UsersTable.addUser(user_id, created_at)
    setCacheValue(key=f'user-{user_id}', value='exists')


def getUserName(user: User) -> str:
    "Generates a string to address the user."

    user_id: int = user.id
    username: str = user.username
    first_name: str = user.first_name
    last_name: str = user.last_name
    
    if first_name:
        if last_name:
            user_name = f'{first_name} {last_name}'
        else:
            user_name = first_name
    elif username:
        user_name = f'@{username}'
    else:
        user_name = f'User №{user_id}'

    return user_name
