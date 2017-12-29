from flask import current_app
import jwt

from invmanager.auth.models import User, Token


def check_token(token: bytes) -> User:
    """Checks a token from a request

    Checks its hasn't expired. Performed by pyJWT
    """
    decoded = jwt.decode(token, verify=True, key=current_app.config.get('SECRET_KEY'))

    if 'token_id' not in decoded:
        raise jwt.InvalidTokenError()

    token_id = decoded['token_id']

    t = Token.query.get(token_id)

    if t is not None:
        return t.user
