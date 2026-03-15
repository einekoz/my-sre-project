import os
import google.generativeai as genai

def get_gemini_review(diff_content):
    # 設定 API Key
    genai.configure(api_key=os.environ.get("gemini-api-key"))    
    # 選擇模型（flash 速度快且便宜，適合做 CI/CD）
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    你是一位資深的 SRE 與資安專家。請針對以下程式碼的 git diff 內容進行審核：
    1. 找出潛在的安全性漏洞（如 SQL 注入、硬編碼金鑰、不安全的 API 暴露）。
    2. 提供程式碼優化建議（效能、可讀性）。
    3. 特別針對 FastAPI 的異步處理與 face_recognition 的資源消耗給予建議。

    代碼差異如下：
    {diff_content}
    """
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    if os.path.exists("change.diff"):
        with open("change.diff", "r") as f:
            diff = f.read()
        print(get_gemini_review(diff))
    else:
        print("找不到 diff 檔案，跳過審核。")