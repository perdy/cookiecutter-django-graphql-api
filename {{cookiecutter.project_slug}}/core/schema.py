import graphene


class Query(recipes.schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
