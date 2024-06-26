# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 eclipse-temurin:17-jdk-jammy

WORKDIR /app

COPY .mvn/ .mvn
COPY mvnw pom.xml ./
COPY libs ./libs
RUN ./mvnw dependency:resolve

COPY src ./src

CMD ["./mvnw", "-Denvironment=localDev", "spring-boot:run"]