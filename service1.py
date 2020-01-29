import uvicorn

from ariadne import QueryType
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import FederatedObjectType, make_federated_schema

type_defs = """
  type Query {
    me: User
  }

  type User @key(fields: "email") {
    id: ID!
    name: String
    email: String!
  }
"""

query = QueryType()
user = FederatedObjectType("User")


@query.field("me")
def resolve_me(_, info):
    return users[0]


@user.reference_resolver
def resolve_user_reference(_, _info, representation):
    return get_user_by_email(representation.get("email"))


schema = make_federated_schema(type_defs, [query, user])
application = GraphQL(schema)

users = [
    {"id": 1, "name": "Ada Lovelace", "email": "ada@example.com"},
    {"id": 2, "name": "Alan Turing", "email": "alan@example.com"},
]


def get_user_by_email(email: str):
    return next((user for user in users if user["email"] == email), None)


if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5001)
