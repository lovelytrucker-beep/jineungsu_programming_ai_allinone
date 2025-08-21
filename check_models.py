# 파일명: check_models.py (jineungsu_ai 폴더에 저장)
from openai import OpenAI
client = OpenAI()                 # 방금 set 한 OPENAI_API_KEY를 읽습니다.
models = client.models.list()
for m in models.data:
    print(m.id)
