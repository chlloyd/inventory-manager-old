import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

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
    token = info.context.session.get('token')

    if not token:
        return

    id = 1  # TODO JWT STUFF
    user = User.query.get(id)
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

    def resolve_users(self, info):
        return User.query.all()


class Login(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, password):
        print(info)


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
