import json
import os
import openai

# 這是一個示例 notify 函式
def notify():
    return "已經透過系統成功發出違規單!"

def check_violation_count():
      # 讀取 CSV 文件來計算違規次數
    violation_count = 0
    total_count = 0
    with open("log2.csv", "r") as f:
        for line in f:
            total_count += 1
            if "Not" in line:
                violation_count += 1

    return violation_count, total_count

def chat(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    violation_count, total_count = check_violation_count()
           # 使用 LLM 來判斷意圖
    prompt = f"""你是一個工安管理師，請根據用戶的要求提供回覆。
    目前的違規次數/抽查次數為 {violation_count}/{total_count}。
    以下是用戶的查詢: "{text}"。請根據查詢內容判斷用戶的意圖並回答：
    1. 如果用戶正在詢問違規情況，請回答"詢問違規情況"。
    2. 如果用戶正在指示管理師發送違規單，請回答"發送違規單"。
    3. 如果都不是，請回答"無法識別"。
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        temperature=0.3,
        messages=[{"role": "system", "content": prompt}],
                 )
                   # 從模型回答中提取意圖
    intent = response.choices[0].message.content
      # 根據模型識別的意圖進行後續處理
    if intent == "詢問違規情況":
           # 進行違規情況的處理
            # 這裡可以加入相關的處理邏輯，例如讀取和分析日誌文件
        prompt = f"""根據最近的安全檢查記錄，共有 {total_count} 次檢查，其中有 {violation_count} 次發現工人沒有佩戴安全帽。如果比例超過 50%，這是一個嚴重的安全問題，你需要建議用戶發送違規單。現在有一位用戶詢問關於違規情況的具體信息，請根據提供的數據，以專業和詳細的方式回答用戶的詢問。"""
        response = openai.chat.completions.create(
            model="gpt-4",
            temperature=0.3,
            messages=[{"role": "system", "content": prompt}],
                                                      )
        return (response.choices[0].message.content)
    elif intent == "發送違規單":
        # 調用 notify 函式發送違規單
        response = notify()
        return response
    else:
              # 用戶意圖無法識別或不屬於上述兩種情況
        return "抱歉，無法識別您的查詢意圖。"

    return "抱歉，無法識別您的查詢意圖。"
