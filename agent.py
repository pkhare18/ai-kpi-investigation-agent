from dotenv import load_dotenv
from openai import OpenAI
import os
 
# Load env variables
load_dotenv()
 
# NVIDIA client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)
 
# Working NVIDIA model
MODEL_NAME = "meta/llama-3.1-8b-instruct"
 
 
def load_agent_md():
    with open("AGENT.md", "r") as f:
        return f.read()
 
 
def ask_llm(prompt: str) -> str:
 
    system_prompt = load_agent_md()
 
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=800
    )
 
    return completion.choices[0].message.content
 
 
# Quick test
if __name__ == "__main__":
 
    result = ask_llm(
        "Taxi trips increased significantly on weekends."
    )
 
    print(result)