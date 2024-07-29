# 1. Use the official OpenJDK image as the base image
FROM openjdk:21-jdk

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy Gradle wrapper and build scripts to the working directory
COPY gradlew gradlew
COPY gradle gradle
COPY build.gradle build.gradle
COPY settings.gradle settings.gradle

# 4. Ensure Gradle wrapper has execute permissions
RUN chmod +x gradlew

# 5. Copy the source code to the working directory
COPY src src

# 6. Run the Gradle build to create the jar file
RUN ./gradlew build

# 7. Copy the generated jar file to the container
COPY build/libs/*.jar app.jar

# 8. Specify the command to run the jar file
ENTRYPOINT ["java", "-jar", "app.jar"]
