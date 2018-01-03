from abc import abstractmethod

from flask import current_app, Request, Response
import jwt

from invmanager.auth.exceptions import AuthorisationError
from invmanager.auth.models import User, Token, db


class AuthMethod:
    """
    Base Class of object that will allow for multiple methods of authentication to be used depending on
    the type of config.

    For example to use GraphiQL, we require that a cookie method be taken so that cookie is passed on each AJAX request.

    But in production, we may want to use an Authorization Header.
    """

    @abstractmethod
    def get_token(self, request: Request) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def set_token(self, response: Response, token: bytes):
        raise NotImplementedError()


class CookieAuth(AuthMethod):
    def get_token(self, request: Request) -> bytes:
        return request.cookies.get('token')

    def set_token(self, response: Response, token: bytes):
        response.set_cookie('token', token)


class AuthHeader(AuthMethod):
    def get_token(self, request: Request) -> bytes:
        return request.headers.get('Authorization')

    def set_token(self, response: Response, token: bytes):
        response.headers.set('Authorization', token)

_auth_methods = {
    'COOKIE': CookieAuth,
    'HEADER': AuthHeader,
}


def get_token(request : Request) -> bytes:
    method = current_app.config.get('AUTH_METHOD')

    method = _auth_methods[method]

    return method().get_token(request)


def set_token(response: Response, token: bytes) -> None:
    method = current_app.config.get('AUTH_METHOD')

    method = _auth_methods[method]

    return method().set_token(response, token)


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
