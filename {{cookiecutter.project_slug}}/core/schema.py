# Add your GraphQL queries here

import graphene

class Query(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
