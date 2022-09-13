pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
//                 sh '''apt-get install python
//                       python -m venv venv
//                       source /venv/bin/activate
//                       pip install -r requirements.txt
//                 '''
                sh 'pip install -r requirements.txt'
                sh 'pytest test.py --aluredir=test-results/'
//                 sh 'rm -rf venv'
            }
        }
    }
}