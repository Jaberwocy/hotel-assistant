# Hotel Assistant 🏨

AI-powered assistant for hotel "У Михалича" built with Python and Groq API.

## What it does

- Answers guest questions about rooms and prices
- Provides information about hotel services
- Detects intent and structures responses as JSON
- Escalates complex requests to human staff
- Remembers conversation history per user

## Rooms & Pricing

| Room Type | 1 Guest | 2 Guests |
|-----------|---------|----------|
| Standard  | $100    | $150     |
| Semi-Lux  | $150    | $200     |
| Lux       | $300    | $350     |

## Services

Restaurant, Café, Parking, Pool, Sauna, Gym, Wi-Fi

## Tech Stack

- Python
- Groq API (llama-3.3-70b)
- JSON structured output

## Example

```python
ask_hotel("Скільки коштує люкс на двох?")

# Output:
# Intent: price_inquiry
# Response: Люкс для двох гостей коштує $350 на ніч.
# Needs human: False
```

## Setup

1. Clone the repo
2. Add your Groq API key
3. Run `hotel_assistant.py`
