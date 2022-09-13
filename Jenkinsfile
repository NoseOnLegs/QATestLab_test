pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python3 -m pytest --alluredir=allure-results test.py'
                sh 'zip -r results.zip allure-results'
                sh 'mv results.zip $HOME/Documents'
            }
        }
    }
}