def get_weather(city: str) -> dict:
    """영어로 도시의 이름이 전달되면, 도시의 현재 날씨 정보를 가져옵니다.

    Args:
        city (str): 도시 이름 (예: "New York", "London", "Tokyo").

    Returns:
        dict: 날씨 정보를 담은 딕셔너리입니다.
              'status' 키는 'success' 또는 'error' 값을 가집니다.
              'success'인 경우 'report' 키에 날씨 설명이 포함됩니다.
              'error'인 경우 'error_message' 키에 오류 메시지가 포함됩니다.
    """
    print(f"--- Tool: get_weather called for city: {city} ---") # Log tool execution
    city_normalized = city.lower().replace(" ", "") # Basic normalization

    # Mock weather data
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

# Example tool usage (optional test)
print("======= TOOL TEST START =============")
print(get_weather("New York"))
print(get_weather("Paris"))
print("======= TOOL TEST DONE =============")
