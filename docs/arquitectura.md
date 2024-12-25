# Arquitectura del Sistema

El sistema está compuesto por múltiples microservicios que se comunican a través de un API Gateway y eventos asincrónicos.

## Diagrama General

```mermaid
graph TD
    subgraph Frontend
        Angular[Angular App]
    end

    subgraph Backend
        APIGateway[API Gateway]
        Usuarios[Microservicio de Usuarios]
        Imagenes[Microservicio Imagenes]
    end

    Angular --> APIGateway
    APIGateway --> Usuarios
    APIGateway --> Imagenes
