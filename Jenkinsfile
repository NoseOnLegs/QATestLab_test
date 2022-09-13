pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh '''
//                       python3 -m venv venv
//                       source /venv/bin/activate
                      pip install -r requirements.txt
                '''
//                 sh 'pip install -r requirements.txt'
                sh 'python3 -m pytest test.py --aluredir=test-results/'
//                 sh 'rm -rf venv'
            }
        }
    }
}