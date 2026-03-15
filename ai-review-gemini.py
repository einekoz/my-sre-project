import os
import sys
from google import genai

def get_gemini_review(diff_content):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "DEBUG: 失敗，找不到 API Key"

    # 1. 移除 http_options，讓 SDK 使用預設穩定的 v1beta 端點
    # 2. 或是明確指定不帶 'models/' 前綴的名稱
    client = genai.Client(api_key=api_key)
    
    # 嘗試最標準的模型 ID 格式
    model_id = "gemini-1.5-flash"
    
    prompt = f"你是一位 SRE 專家，請審核以下代碼差異並給予建議：\n{diff_content}"
    
    try:
        print(f"DEBUG: 正在向模型 {model_id} 發送請求...")
        # 直接使用簡潔的調用
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        print("DEBUG: 請求成功")
        return response.text
    except Exception as e:
        # 如果還是失敗，嘗試列出模型清單，這能徹底找出問題
        try:
            available_models = [m.name for m in client.models.list()]
            return f"DEBUG: 發生錯誤。可用模型清單前三個為: {available_models[:3]}。錯誤內容: {str(e)}"
        except:
            return f"DEBUG: 發生例外錯誤: {str(e)}"

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