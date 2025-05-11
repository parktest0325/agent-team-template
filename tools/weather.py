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




from google.adk.tools.tool_context import ToolContext

def set_temperature_unit(unit: str, tool_context:ToolContext) -> bool:
    """현재 세션의 선호하는 온도 단위를 변경합니다.
    Args:
        unit: 반드시 Celsius 또는 Fahrenheit 값만 들어와야 한다.
    Return:
        변경 성공 시 True, 아니면 False
    """
    if unit not in ("Celsius", "Fahrenheit"):
        return False
    tool_context.state["user_preference_temperature_unit"] = unit
    return True



def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """날씨 정보를 가져오고, 세션 상태에 따라 온도 단위를 변환합니다."""
    print(f"--- Tool: get_weather_stateful called for {city} ---")

    # --- State로부터 선호도 확인 ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # 기본은 섭씨로 설정
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    city_normalized = city.lower().replace(" ", "")

    # Mock 날씨 데이터(모두 섭씨로 저장)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # State 선호도에 따라 포맷팅 수행
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32 # 화씨 계산
            temp_unit = "°F"
        else: # 기본은 섭씨
            temp_value = temp_c
            temp_unit = "°C"

        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        # 상태에 값을 다시 저장하는 예시 (이 도구에서는 선택 사항)
        tool_context.state["last_city_checked_stateful"] = city
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        # 도시를 못찾는 경우 처리
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        print(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}
