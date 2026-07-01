from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq = Groq()

def classify_with_llm(logs):
    prompt = f"""You are a log classification assistant. Your task is to classify log messages into one of the following categories: "Workflow error", "Deprecation Warning".
    If you can't classify the log message into either of these categories, return "Unclassified". Only return the category name without any explanation or additional text.
    Log message: {logs}"""
    response = groq.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    log_messages = ["Case escalation for ticket ID 7324 failed because the assigned support agent is       no longer active.", 
    "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality.", 
    "Admin access escalation detected for user 9429"]
    for log_message in log_messages:
        label = classify_with_llm(log_message)
        print(label)