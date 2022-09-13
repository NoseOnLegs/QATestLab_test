pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python3 -m pytest test.py --aluredir=test-results/'
            }
        }
    }
}