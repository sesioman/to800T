# System Architecture

The system is composed of multiple microservices that communicate through an API Gateway and asynchronous events.

## General Diagram

```mermaid
graph TD
    subgraph Frontend
        Angular[Angular App]
    end

    subgraph Backend
        APIGateway[API Gateway]
        Users[User Microservice]
        Images[Images Microservice]
    end

    Angular --> APIGateway
    APIGateway --> Users
    APIGateway --> Images
