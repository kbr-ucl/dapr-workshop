# Dapr Workshop - introduction

![Dapr sidecar](imgs/dapr_sidecar_pixelart.png)

Welcome to Diagrid's [Dapr](https://dapr.io/) Workshop! This repository contains a set of hands-on challenges designed to introduce you to Dapr's most popular APIs and give you a starting point to build your own distributed applications.

Microservices architectures are popular for a variety of reasons - they enable polyglot development, are easily scaled, and perform simple, focused tasks. However, as the number of microservices grows, so does the complexity of the system. Managing security, observability, and resiliency becomes increasingly challenging, often leading to the same problems being solved over and over again.

Dapr addresses these challenges by providing a set of APIs for building distributed systems with best practices for microservices baked in. Leveraging Dapr allows you to reduce development time while building reliable, observable, and secure distributed applications with ease. Let’s dive in and explore how Dapr can simplify your journey to distributed systems excellence!

![Dapr from dev to hosting](imgs/dapr-slidedeck-overview.png)

## Goals

On completion of this workshop, you will understand how three of the most popular Dapr Building Block APIs work: [State Management](https://docs.dapr.io/developing-applications/building-blocks/state-management/), [Service Invocation](https://docs.dapr.io/developing-applications/building-blocks/service-invocation/), [Publish/Subscribe](https://docs.dapr.io/developing-applications/building-blocks/pubsub/), and [Workflow](https://docs.dapr.io/developing-applications/building-blocks/workflow/).

You will build five microservices to simulate the process of ordering a pizza:

- The `pizza-storefront` service serves as an entry point for customers to order a new pizza.
- The `pizza-kitchen` service has a single responsibility, to cook the pizza.
- The `pizza-delivery` service manages the delivery process, from picking up the pizza at the kitchen to delivering it to the customer's doorstep.
- The `pizza-order` service manages the order status in the state store.
- The `pizza-workflow` service orchestrates the order steps, from ordering to delivery.

## Challenges

### Challenge 1: State Management

You will start the workshop by creating the `pizza-order` service. It is responsible for managing the  order state and saving it to a Redis database, using the [Dapr State Management Building Block](https://docs.dapr.io/developing-applications/building-blocks/state-management/). You will learn how to create a Dapr Component specification, and how to use the Dapr SDK to save and retrieve an item using the State Store API.

<img src="imgs/challenge-1.png" width=50%>

### Challenge 2: Service Invocation

This challenge will focus on synchronous communication between services using the [Dapr Service Invocation Building Block](https://docs.dapr.io/developing-applications/building-blocks/service-invocation/). After the pizza order is saved in the database, you will create the three following services: `pizza-storefront`, `pizza-kitchen`, and `pizza-delivery`. `pizza-storefront` will invoke the endpoints from the other services to cook and deliver the pizza.

<img src="imgs/challenge-2.png" width=50%>

### Challenge 3: Pub/Sub

In the third challenge, you will add a Pub/Sub component to the `pizza-order` service. You will use the [Dapr Publish & Subscribe Building Block](https://docs.dapr.io/developing-applications/building-blocks/pubsub/) to publish events to a Redis Streams message broker from `pizza-storefront`, `pizza-kitchen`, and `pizza-delivery`. These events represent each stage in the pizza order, cooking, and delivery process. For every event published, the `pizza-order` service will subscribe to it and update the current order status in the Redis State Store.

<img src="imgs/challenge-3.png" width=60%>

### Challenge 4: Workflows

Now you will modify the application to orchestrate the process of ordering, cooking, and delivering the pizza to use [Dapr's Workflow Building Block](https://docs.dapr.io/developing-applications/building-blocks/workflow/). With that you will guarantee that every step happens in a particular order. A validation state will also be created to guarantee that the pizza was cooked properly before it is delivered.

<img src="imgs/workflow.png" width=75%>

## Get started

No existing knowledge of Dapr or microservices is needed to complete this workshop but basic programming skills for your language of choice are required.
Today this workshop offers challenges in .NET and Python. Complete the technical prerequisites and start the first challenge!
