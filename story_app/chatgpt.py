import openai

openai.api_key = '4b98eCipWEd7272fuiZlnZtjLaatiCWm2di3cdVoXxHskiyxuYdCr7-WS94fu0gbbmg5QheHOQVinJiZnwGCTgw'  # 自分のAPIキーに置き換えてください

def generate_response(input_text):
    response = openai.Completion.create(
        engine="text-davinci-002",  # 使用するGPT-3エンジンを指定
        prompt=input_text,
        max_tokens=1500  # 応答の最大トークン数を設定
    )
    
    return response.choices[0].text.strip()
