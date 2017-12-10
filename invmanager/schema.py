from graphene import ObjectType, Schema

from .auth.schema import AuthQuery, AuthMutation


class Query(AuthQuery, ObjectType):
    pass


class Mutation(AuthMutation, ObjectType):
    pass


schema = Schema(query=Query)
