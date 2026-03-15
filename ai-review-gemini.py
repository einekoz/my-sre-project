import os
import sys
from google import genai

def get_gemini_review(diff_content):
    # 從環境變數讀取 API Key (SRE 最佳實踐，避免硬編碼)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "錯誤：找不到 GEMINI_API_KEY 環境變數。"

# 偵錯用：印出 key 的長度（不要印出內容，以免洩漏在 Log）
    if api_key:
        print(f"DEBUG: 成功讀取 API Key，長度為: {len(api_key)}")
    else:
        print("DEBUG: Python 腳本內依然抓不到 GEMINI_API_KEY")
        return "錯誤：找不到 GEMINI_API_KEY 環境變數。"

    # 初始化最新的 GenAI Client
    client = genai.Client(api_key=api_key)
    
    # 使用最新的模型名稱格式
    model_id = "gemini-1.5-flash"
    
    prompt = f"""
    你是一位資深的 SRE 與資安專家。請針對以下程式碼的 git diff 內容進行審核：
    1. 找出潛在的安全性漏洞（如 SQL 注入、硬編碼金鑰、不安全的 API 暴露）。
    2. 提供程式碼優化建議（效能、可讀性）。
    3. 特別針對 FastAPI 的異步處理與 face_recognition 的資源消耗給予建議。

    代碼差異如下：
    {diff_content}
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI 審核過程發生錯誤：{str(e)}"

if __name__ == "__main__":
    diff_file = "change.diff"
    if os.path.exists(diff_file):
        with open(diff_file, "r", encoding="utf-8") as f:
            diff = f.read()
        
        if not diff.strip():
            print("Diff 內容為空，跳過審核。")
        else:
            print("--- Gemini AI Code Review Report ---")
            print(get_gemini_review(diff))
    else:
        print(f"找不到 {diff_file} 檔案，跳過審核。")