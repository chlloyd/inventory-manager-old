from flask import request
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from .authentication import check_token, get_token, set_token
from .decorators import after_request
from .exceptions import AuthorisationError
from .models import User, db


def create_user(name, email, password):
    u = User()
    u.name = name
    u.email = email
    u.password = password

    db.session.add(u)
    db.session.commit()

    return u


def get_user(info):
    token = get_token(info.context)

    if not token:
        return

    user = check_token(token)
    if user is None:
        pass

    return user


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude_fields = ('password_hash',)


class AuthQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    users = graphene.List(UserType)

    def resolve_me(self, info):
        user = get_user(info)

        if user is None:
            raise AuthorisationError("Incorrect username/password combination")

        return user

    def resolve_users(self, info):
        return User.query.all()


class Login(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, password):
        u = User.query.filter_by(email=email).first()

        if u is not None:
            if u.verify_password(password):
                token = u.generate_token()

                @after_request
                def defer_set_token(response):
                    set_token(response, token)

                return Login(user=u)
        raise Exception("User / Password Combination")


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, name, email, password):
        # TODO: Check current user has admin rights
        user = create_user(name, email, password)
        return CreateUser(user)


class AuthMutation(object):
    login = Login.Field()
