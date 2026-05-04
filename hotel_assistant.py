import requests
import json

API_KEY = "твій_ключ_сюди"

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

system_prompt = """
Ти асистент готелю "У Михалича". Відповідай ввічливо і професійно українською мовою.

Номери та ціни за ніч:
- Стандарт: 1 гість $100, 2 гості $150
- Напівлюкс: 1 гість $150, 2 гості $200
- Люкс: 1 гість $300, 2 гості $350

Послуги готелю: ресторан, кафе, паркінг, басейн, сауна, спортзал, Wi-Fi.

Завжди повертай відповідь ТІЛЬКИ у форматі JSON і нічого більше:
{
  "intent": "тип запиту",
  "response": "твоя відповідь гостю",
  "needs_human": false
}

Можливі значення intent: price_inquiry, availability, services, checkout, other
needs_human встановлюй true якщо запит складний або незрозумілий.
"""

def ask_hotel(question):
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, json=body)

    if response.ok:
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        parsed = json.loads(answer)
        print(f"Intent: {parsed['intent']}")
        print(f"Response: {parsed['response']}")
        print(f"Needs human: {parsed['needs_human']}")
        print("---")
    else:
        print(f"Помилка: {response.status_code}", response.text)

ask_hotel("Скільки коштує люкс на двох?")
ask_hotel("Чи є у вас басейн?")
ask_hotel("Хочу поскаржитись на сусідів")
