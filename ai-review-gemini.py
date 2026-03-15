import os
import sys
from google import genai

def get_gemini_review(diff_content):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "DEBUG: 失敗，找不到 API Key"

    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    
    prompt = f"請針對以下程式碼差異提供簡短的 SRE 建議：\n{diff_content}"
    
    try:
        # 強制印出進度
        print("DEBUG: 正在向 Gemini 發送請求...")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        print("DEBUG: 請求成功，準備印出結果")
        return response.text
    except Exception as e:
        return f"DEBUG: 發生例外錯誤: {str(e)}"

if __name__ == "__main__":
    # 強制將輸出流設為無緩衝
    sys.stdout.reconfigure(line_buffering=True)
    
    print("DEBUG: 腳本啟動")
    if os.path.exists("change.diff"):
        with open("change.diff", "r") as f:
            diff = f.read()
        
        # 只要檔案有東西就執行
        if len(diff.strip()) > 0:
            result = get_gemini_review(diff)
            print("\n=== Gemini Review Result ===")
            print(result)
            print("============================\n")
        else:
            print("DEBUG: diff 檔案內容為空")
    else:
        print("DEBUG: 找不到 change.diff")