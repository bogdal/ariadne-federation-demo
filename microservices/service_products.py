import uvicorn

from ariadne import ObjectType, QueryType
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import FederatedObjectType, make_federated_schema

type_defs = """
  type Query {
    topProducts(first: Int = 5): [Product]
  }

  type Product @key(fields: "upc") {
    upc: String!
    name: String
    price: Int
    weight: Int
  }
"""

query = QueryType()
product = FederatedObjectType("Product")


@query.field("topProducts")
def resolve_top_products(*_, first):
    return products[:first]


@product.reference_resolver
def resolve_product_reference(_, _info, representation):
    return get_product_by_upc(representation["upc"])


schema = make_federated_schema(type_defs, [query, product])
application = GraphQL(schema)


products = [
    {"upc": "1", "name": "Table", "price": 899, "weight": 100},
    {"upc": "2", "name": "Couch", "price": 1299, "weight": 1000},
    {"upc": "3", "name": "Chair", "price": 54, "weight": 50},
]


def get_product_by_upc(upc: str):
    return next((product for product in products if product["upc"] == upc), None)


if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5003)
