# Ariadne Federation Demo

It's an example of the use of Apollo Federation in Ariadne.

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

The last thing is to run the gateway:

```bash
npm run start-gateway
```
Gateway will be available at http://localhost:4000



## Example queries


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
}
```

```graphql
query {
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
