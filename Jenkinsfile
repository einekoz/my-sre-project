pipeline {
    agent any 
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key') // 從 Jenkins 的憑證管理中取得 API Key
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Generate Diff') {
            steps {
                // 確保 git diff 有內容，若沒差異會報錯，這裡加個 || true 預防
                sh 'git diff HEAD~1 HEAD > change.diff || echo "No changes" > change.diff'
            }
        }
        stage('AI Code Review') {
            steps {
                // 現在系統已經有 python3 了！
                sh 'python3 ai-review-gemini.py'
            }
        }
    }
}