pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pytest test.py --aluredir=test-results/'
            }
        }
    }
}