from django.urls import path

from core.schema import schema
from core.views import DRFAuthenticatedGraphQLView

app_name = 'core'
urlpatterns = [
    path('graphql/', DRFAuthenticatedGraphQLView.as_view(graphiql=True, schema=schema)),
]
