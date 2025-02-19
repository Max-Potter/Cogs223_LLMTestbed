import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
key = os.getenv("DEEPSEEK_KEY")
print(key)
