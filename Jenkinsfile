pipeline {
    agent any
    environment {
        // 從 Jenkins 憑證取得 API Key
        GEMINI_API_KEY = credentials('gemini-api-key')
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
            agent {
                docker { image 'python:3.9-slim' } // 動態啟動一個 python 環境
            }
            steps {
                // 安裝依賴並執行
                sh 'pip install google-generativeai'
                sh 'python3 ai-review-gemini.py'
            }
        }
    }
}