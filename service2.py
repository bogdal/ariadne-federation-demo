import uvicorn

from ariadne import ObjectType, QueryType
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import FederatedObjectType, make_federated_schema

type_defs = """
  type Query {
    hello: String
  }

  type Review @key(fields: "id") {
    id: ID!
    body: String
    author: User @provides(fields: "email")
    product: Product @provides(fields: "upc")
  }

  type User @key(fields: "email") @extends {
    email: String! @external
    reviews: [Review]
  }

  type Product @key(fields: "upc") @extends {
    upc: String! @external
    reviews: [Review]
  }
"""

query = QueryType()
review = FederatedObjectType("Review")
user = FederatedObjectType("User")
product = FederatedObjectType("Product")


@review.reference_resolver
def resolve_reviews_reference(_, _info, representation):
    return get_review_by_id(representation["id"])


@review.field("author")
def resolve_review_author(review, *_):
    return {"__typename": "User", "email": review["user"]["email"]}


@review.field("product")
def resolve_review_product(review, *_):
    return {"__typename": "Product", "upc": review["product"]["upc"]}


@user.field("reviews")
def resolve_user_reviews(representation, *_):
    return get_user_reviews(representation["email"])


@product.field("reviews")
def resolve_product_reviews(representation, *_):
    return get_product_reviews(representation["upc"])


schema = make_federated_schema(type_defs, [query, user, review, product])
application = GraphQL(schema)


reviews = [
    {
        "id": "1",
        "user": {"email": "ada@example.com"},
        "product": {"upc": "1"},
        "body": "Love it!",
    },
    {
        "id": "2",
        "user": {"email": "ada@example.com"},
        "product": {"upc": "2"},
        "body": "Too expensive.",
    },
    {
        "id": "3",
        "user": {"email": "alan@example.com"},
        "product": {"upc": "2"},
        "body": "Could be better.",
    },
]


def get_review_by_id(id: int):
    return next((review for review in reviews if review["id"] == id), None)


def get_user_reviews(email: str):
    return [review for review in reviews if review["user"]["email"] == email]


def get_product_reviews(upc: str):
    return [review for review in reviews if review["product"]["upc"] == upc]


if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5002)
