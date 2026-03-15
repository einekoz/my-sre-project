import os
import sys
from google import genai

def get_gemini_review(diff_content):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "DEBUG: 失敗，找不到 API Key"

    client = genai.Client(api_key=api_key)
    
    # 根據你的 ListModels 輸出，使用最新、最穩定的模型 ID
    model_id = "gemini-2.5-flash"
    
    prompt = f"""
    你是一位資深的 SRE 與資安專家。請針對以下程式碼的 git diff 內容進行審核：
    1. 找出潛在的安全性漏洞。
    2. 提供程式碼優化建議（效能、可讀性）。
    3. 特別針對 FastAPI 的異步處理與 face_recognition 的資源消耗給予建議。

    代碼差異如下：
    {diff_content}
    """
    
    try:
        print(f"DEBUG: 正在向最新模型 {model_id} 發送請求...")
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        print("DEBUG: 請求成功！")
        return response.text
    except Exception as e:
        return f"DEBUG: 嘗試使用 {model_id} 依然失敗: {str(e)}"

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    print("DEBUG: 腳本啟動")
    
    if os.path.exists("change.diff"):
        with open("change.diff", "r", encoding="utf-8") as f:
            diff = f.read()
        
        if len(diff.strip()) > 0:
            print(f"DEBUG: 準備審核，Diff 長度: {len(diff)}")
            result = get_gemini_review(diff)
            print("\n=== Gemini Review Result ===")
            print(result)
            print("============================\n")
        else:
            print("DEBUG: diff 檔案內容為空")
    else:
        print("DEBUG: 找不到 change.diff")