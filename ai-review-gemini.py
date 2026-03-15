import os
from google import genai
from google.genai import types # 引入型別定義

def get_gemini_review(diff_content):
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 初始化 Client，並明確指定使用 v1 版本 (避開 v1beta 的路徑問題)
    client = genai.Client(
        api_key=api_key,
        http_options={'api_version': 'v1'} 
    )
    
    # 確保模型名稱正確
    model_id = "gemini-1.5-flash"
    
    prompt = f"""
    你是一位資深的 SRE 與資安專家。請針對以下程式碼的 git diff 內容進行審核：
    1. 找出潛在的安全性漏洞。
    2. 提供程式碼優化建議（效能、可讀性）。
    3. 特別針對 FastAPI 的異步處理與 face_recognition 的資源消耗給予建議。

    代碼差異如下：
    {diff_content}
    """
    
    try:
        # 明確調用方式
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text
    except Exception as e:
        # 如果 v1 還是不行，嘗試列出所有可用模型，這能幫我們診斷
        try:
            models = [m.name for m in client.models.list()]
            return f"模型錯誤。可用模型清單：{models}。錯誤訊息：{str(e)}"
        except:
            return f"AI 審核發生異常：{str(e)}"