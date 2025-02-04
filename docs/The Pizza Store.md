# The Pizza Store

The Pizza Store application simulates placing a Pizza order that is going to be processed by different services. The application is composed by the Pizza Store Service which serves as the front-end and back-end to place the order. The order is sent to the Kitchen Service for preparation and once the order is ready to be delivered the Delivery Service takes the order to your door.

[![Architecture](https://github.com/diagrid-labs/conductor-pizza-store/raw/main/imgs/distr-pizza-store-architecture-v1.png)](https://github.com/diagrid-labs/conductor-pizza-store/blob/main/imgs/distr-pizza-store-architecture-v1.png)

These services will need to store and read data from a state store, and exchange messages via a message broker to enable asynchronous communication.