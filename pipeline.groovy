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
        
        stage('Git Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Tyranno-Rex/portfoilo-oracle.git'
            }
        }
    }
}