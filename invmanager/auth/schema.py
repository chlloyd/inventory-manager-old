import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import User


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User


class AuthQuery(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return User.query.all()


class Login(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        pass


class AuthMutation(object):
    login = Login.Field()
