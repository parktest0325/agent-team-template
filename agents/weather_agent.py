from tools.weather import get_weather
from constant import MODEL_GEMINI_2_0_FLASH
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

AGENT_MODEL = MODEL_GEMINI_2_0_FLASH # Gemini로 시작

session_service = InMemorySessionService()
APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

# 명확하고 구체적인 instruction 프롬프트를 제공하세요. 지침이 자세할수록 LLM은 자신의 역할과 도구 사용 방법을 더 잘 이해할 수 있습니다. 필요하다면 오류 처리 방식도 명시적으로 작성하세요.
# 설명적인 name과 description 값을 선택하세요. 이는 ADK 내부적으로 사용되며, 이후 자동 위임 기능(뒤에서 다룸)에 매우 중요합니다.

weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL, # Gemini인 경우 문자열, LiteLLM인 경우 객체
    description="특정 도시의 날씨 정보를 제공합니다.",   # 다른 에이전트가 이 에이전트에 작업을 위임할때 이 설명을 보기 때문에 중요함. 
    instruction="당신은 친절한 날씨 도우미입니다. "                # 시스템 프롬프트와 마찬가지임. 페르소나나 목표, 툴 사용법 등
                "사용자가 특정 도시의 날씨를 물어보면, "
                "반드시 'get_weather' 도구를 사용해 정보를 조회하세요. "
                "도구에서 오류가 발생하면 정중하게 사용자에게 알려주세요. "
                "정상적으로 정보를 받으면, 명확하고 보기 좋게 날씨 정보를 전달하세요.",
    tools=[get_weather], # 함수를 직접 전달
)

print(f"Agent '{weather_agent.name}' created using model '{AGENT_MODEL}'.")


session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
print(f"Session created: App='{APP_NAME}, User='{USER_ID}', Session='{SESSION_ID}'")

# runner 가 사용자/세션 컨텍스트랑 Content로 감싼 메시지를 달하면서 run_async를 호출한다.
# 그렇게되면 러너가 지혼자 Event들을 반복(iterate) 하면서 에이전트의 각 실행 단계(도구호출, 도구결과수신, 중간LLM 사고 등)를 반복하는 것이다.
# event.is_final_response() 함수로 최종 응답 이벤트를 식별하고 출력
weather_runner = Runner(
    agent=weather_agent,
    app_name=APP_NAME,
    session_service=session_service
)
