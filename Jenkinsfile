pipeline {
    agent any 
    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY') // 從 Jenkins 的憑證管理中取得 API Key
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
                withCredentials([string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')]) {
                    sh '''
                        export GEMINI_API_KEY=${GEMINI_API_KEY}
                        echo "--- 檢查開始 ---"
                        # 強制輸出不緩衝，並顯示 diff 檔案大小
                        ls -lh change.diff
                        python3 -u ai-review-gemini.py
                        echo "--- 檢查結束 ---"
                    '''
                }
            }
        }
    }   
}