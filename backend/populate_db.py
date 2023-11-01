import logging
from datalayer_user import UserDataLayer

def test_user_creation():
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')

test_user_creation()