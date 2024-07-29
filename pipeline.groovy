// ------------------------------------------------------------------------ //
// This is the Jenkins pipeline script that will be used to build the       //
// Docker images and run the containers.                                    //
// The pipeline will be triggered by a webhook from the GitHub repository.  //
// ------------------------------------------------------------------------ //

pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'portfolio-oracle-token',
                    url: 'https://github.com/Tyranno-Rex/portfoilo-oracle.git'
            }
        }
        stage('Clean Workspace') {
            steps {
                sh 'rm -rf *'
            }
        }

        stage('Stop and Delete Containers') {
            steps {
                script {
                    def containerName = 'springboot-container'
                    def containerList = sh(script: "docker ps -a --format '{{.Names}}'", returnStdout: true).trim()
                    if (containerList.contains(containerName)) {
                        sh "docker stop ${containerName}"
                        sh "docker rm ${containerName}"
                    } else {
                        echo "No container with the name ${containerName} found."
                    }
                }
                script {
                    def containerName = 'fastapi-container'
                    def containerList = sh(script: "docker ps -a --format '{{.Names}}'", returnStdout: true).trim()
                    if (containerList.contains(containerName)) {
                        sh "docker stop ${containerName}"
                        sh "docker rm ${containerName}"
                    } else {
                        echo "No container with the name ${containerName} found."
                    }
                }
            }
        }

        stage('Delete Docker Image') {
            steps {
                script {
                    def imageName = 'springboot-image'
                    def imageList = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}'", returnStdout: true).trim()
                    if (imageList.contains(imageName)) {
                        sh "docker rmi ${imageName}"
                    } else {
                        echo "No image with the name ${imageName} found."
                    }
                }
                script {
                    def imageName = 'fastapi-image'
                    def imageList = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}'", returnStdout: true).trim()
                    if (imageList.contains(imageName)) {
                        sh "docker rmi ${imageName}"
                    } else {
                        echo "No image with the name ${imageName} found."
                    }
                }
            }
        }

        stage('Git Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Tyranno-Rex/portfoilo-oracle.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir ('./springboot') {
                    sh 'docker build -t springboot-image .'
                }
                // dir ('./fastapi') {
                //     sh 'docker build -t fastapi-image .'
                // }
            }
        }

        stage ('Check Docker Network') {
            steps {
                script {
                    def networkName = 'docker-network'
                    def networkList = sh(script: "docker network ls --format '{{.Name}}'", returnStdout: true).trim()
                    if (networkList.contains(networkName)) {
                        echo "Network ${networkName} already exists."
                    } else {
                        sh "docker network create ${networkName}"
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name springboot-container --network docker-network -p 8080:8080 springboot-image'
                // sh 'docker run -d --name fastapi-container --network docker-network -p 8000:8000 fastapi-image'
            }
        }
    }
}