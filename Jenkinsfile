pipeline {
    agent any
    environment {
        // 從 Jenkins 憑證取得 API Key
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Generate Diff') {
            steps {
                // 取得目前 commit 與前一個 commit 的差異
                sh 'git diff HEAD~1 HEAD > change.diff'
            }
        }
        stage('AI Code Review') {
            steps {
                sh 'python3 ai-review-gemini.py'
            }
        }
    }
}