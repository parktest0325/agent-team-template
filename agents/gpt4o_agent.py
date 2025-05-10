from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from constant import *
from tools.weather import get_weather
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner


# Step 1에서 정의한 `get_weather` 함수가 현재 환경에 정의되어 있는지 확인하세요.
# 앞서 정의한 `call_agent_async` 함수도 준비되어 있어야 합니다.

# --- Agent using GPT-4o ---
weather_agent_gpt = None # None으로 초기화
gpt_runner = None      # Runner를 None으로 초기화

# 상호작용 컨텍스트를 식별하기 위한 상수를 정의합니다.
APP_NAME_GPT = "weather_tutorial_app_gpt" # 이번 테스트를 위한 고유한 앱이름
USER_ID_GPT = "user_1_gpt"
SESSION_ID_GPT = "session_001_gpt" # 단순함을 위해 고정된 세션ID 사용

# 오류 처리: 에이전트 정의는 try...except 블록으로 감싸줍니다. 이를 통해 특정 제공자의 API 키가 누락되었거나 유효하지 않은 경우 전체 코드 실행이 실패하지 않고, 설정된 모델만으로도 튜토리얼을 계속 진행할 수 있습니다.
try:
    weather_agent_gpt = Agent(
        name="weather_agent_gpt",
        # 핵심 차이점: 모델 식별자를 LiteLlm으로 랩핑
        model=LiteLlm(model=MODEL_GPT_4O),
        description="날씨 정보를 제공합니다 (GPT-4o 사용).",
        instruction="당신은 GPT-4o 기반의 친절한 날씨 도우미입니다. "
                    "도시의 날씨를 요청받으면 'get_weather' 도구를 사용하세요. "
                    "도구의 응답 상태에 따라 성공적인 결과는 명확하게, 오류는 정중한 메시지로 안내하세요.",
        tools=[get_weather], # 동일한 도구 재사용
    )
    print(f"Agent '{weather_agent_gpt.name}' created using model '{MODEL_GPT_4O}'.")
    
    # 이 튜토리얼에서 사용하는 InMemorySessionService는 심플하고, 반영구적인 저장소입니다.
    session_service_gpt = InMemorySessionService() # 전용 서비스를 생성합니다.

    # 대화가 발생할 특정한 Session 생성
    session_gpt = session_service_gpt.create_session(
        app_name=APP_NAME_GPT,
        user_id=USER_ID_GPT,
        session_id=SESSION_ID_GPT
    )
    print(f"Session created: App='{APP_NAME_GPT}', User='{USER_ID_GPT}', Session='{SESSION_ID_GPT}'")

    # 이 에이전트와 해당 세션 서비스를 위한 전용 runner를 생성합니다.
    gpt_runner = Runner(
        agent=weather_agent_gpt,
        app_name=APP_NAME_GPT,       # 특정한 앱이름 사용
        session_service=session_service_gpt # 특정한 Session Service 사용
        )
    print(f"Runner created for agent '{gpt_runner.agent.name}'.")



except Exception as e:
    print(f"❌ Could not create or run GPT agent '{MODEL_GPT_4O}'. Check API Key and model name. Error: {e}")
