pipeline {
    agent {
        docker {
            image 'aerokube/selenoid:1.10.8'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'pytest test.py --aluredir=test-results/'
            }
        }
    }
}