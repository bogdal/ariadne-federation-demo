# Ariadne Federation Demo

This is an example of how to use `Apollo Federation` with [Ariadne](https://ariadnegraphql.org/docs/apollo-federation).

The `microservices` folder contains separate GraphQL services that we want to combine into a single data graph.

### Let's start

First of all, we need to install all required dependencies:

```bash
pip install -r requirements.txt
```
```bash
npm install
```
Now, we can run all of the microservices at once using the following command:

```bash
npm run start-services
```

The last thing is to run the gateway. Open a new terminal window and use:

```bash
npm run start-gateway
```
Gateway will be available at http://localhost:4000



## Example queries

Now we can execute GraphQL operations as if it were implemented as a monolithic service:


```graphql
query {
  me {
    name
    email
    reviews {
      body
      product {
        upc
        name
      }
    }
  }

  topProducts(first: 3) {
    upc
    name
    reviews {
      body
      author {
        name
        email
      }
    }
  }
}
```
