import requests
import json

API_KEY = "твій_ключ_сюди"
TG_TOKEN = "ТГ-токен"

TG_URL = f"https://api.telegram.org/bot{TG_TOKEN}"

system_prompt = """
Ти асистент готелю "У Михалича". Відповідай ввічливо і професійно українською мовою.

Номери та ціни за ніч:
- Стандарт: 1 гість $100, 2 гості $150
- Напівлюкс: 1 гість $150, 2 гості $200
- Люкс: 1 гість $300, 2 гості $350

Послуги готелю: ресторан, кафе, паркінг, басейн, сауна, спортзал, Wi-Fi.

ВАЖЛИВО: Ти знаєш ТІЛЬКИ ту інформацію що написана вище. 
Якщо гість питає про щось чого немає в цьому описі — наприклад ціни на їжу, 
меню, вартість додаткових послуг — відповідай що ця інформація уточнюється 
у менеджера і встановлюй needs_human: true.
Ніколи не вигадуй ціни або інформацію якої немає в описі.
Завжди повертай відповідь ТІЛЬКИ у форматі JSON і нічого більше:
{
  "intent": "тип запиту",
  "response": "твоя відповідь гостю",
  "needs_human": false
}

Можливі значення intent: price_inquiry, availability, services, checkout, other
needs_human встановлюй true якщо запит складний або незрозумілий.
"""

# Словник де ключ - chat_id, значення - історія повідомлень
chat_histories = {}

def ask_hotel(chat_id, question):
    # Якщо цей користувач пише вперше - створюємо порожню історію
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    # Додаємо нове повідомлення в історію
    chat_histories[chat_id].append({
        "role": "user",
        "content": question
    })

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt}
            ] + chat_histories[chat_id]  # додаємо всю історію
        }
    )

    data = response.json()
    answer = data["choices"][0]["message"]["content"]
    parsed = json.loads(answer)

    # Додаємо відповідь бота теж в історію
    chat_histories[chat_id].append({
        "role": "assistant",
        "content": answer
    })

    return parsed

def send_message(chat_id, text):
    requests.post(f"{TG_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def get_updates(offset=None):
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    response = requests.get(f"{TG_URL}/getUpdates", params=params)
    return response.json()

print("Бот запущено...")

offset = None
while True:
    updates = get_updates(offset)
    for update in updates.get("result", []):
        offset = update["update_id"] + 1
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if text:
            print(f"Запит від {chat_id}: {text}")
            result = ask_hotel(chat_id, text)
            response_text = result["response"]
            if result["needs_human"]:
                response_text += "\n\n⚠️ Ваш запит передано менеджеру."
            send_message(chat_id, response_text)
            print(f"Відповідь: {response_text}")
