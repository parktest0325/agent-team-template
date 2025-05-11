from google.adk.runners import Runner
from agents.root_agent import build_weather_root
from services.session import create_session_service

# 상호작용 컨텍스트를 식별하기 위한 상수를 정의합니다.
APP_NAME = "weather_tutorial_agent_team"
USER_ID = "user_1_agent_team"
SESSION_ID = "session_001_agent_team" # 단순함을 위해 고정된 세션ID 사용

def make_runner() -> Runner:
    # 초기 세션 상태 지정
    initial_state = {
        "user_preference_temperature_unit": "Celsius"
    }
    session_service = create_session_service()
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state    # << 초기상태 설정
    )
    retrieved_session = session_service.get_session(app_name=APP_NAME,
                                                         user_id=USER_ID,
                                                         session_id = SESSION_ID)
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")

    root = build_weather_root()
    return Runner(
        agent=root, # 루트 에이전트 객체 사용
        app_name=APP_NAME,       # 특정한 앱 이름 사용
        session_service=session_service # 특정한 세션 서비스 사용
    )