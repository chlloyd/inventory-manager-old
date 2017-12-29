from flask import current_app
import jwt

from invmanager.auth.exceptions import AuthorisationError
from invmanager.auth.models import User, Token, db


def check_token(token: bytes) -> User:
    """Checks a token from a request

    Checks its hasn't expired. Performed by pyJWT
    """
    decoded = jwt.decode(token, verify=True, key=current_app.config.get('SECRET_KEY'),
                         verify_exp=True)

    if 'token_id' not in decoded:
        raise jwt.InvalidTokenError()

    token_id = decoded['token_id']

    t = Token.query.get(token_id)

    if t is None:
        raise AuthorisationError("Invalid Token")
    return t.user


def revoke_token(token_id : str):
    """Stop a JWT token from authenticating.

    Args:
        token_id (str): The tokens token_id field

    Returns:
        bool: True if revoking was successful. False if it was unsuccessful or didn't exist

    """
    t = Token.query.get(token_id)

    if t is None:
        return False

    db.session.delete(t)
    db.session.commit()
    return True
