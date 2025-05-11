from agents.greet_agent import greeting_agent, farewell_agent
from tools.weather import get_weather, get_weather_stateful, set_temperature_unit
from tools.guardrail import block_keyword_guardrail, block_paris_tool_guardrail
from constant import *
from google.adk.agents import Agent
from google.adk.runners import Runner

from google.adk.sessions import InMemorySessionService

# 루트 에이전트를 정의하기 전에 하위 에이전트들이 정상적으로 생성되었는지 확인하세요.
# 또한, 'get_weather' 도구가 정의되어 있는지도 확인하세요.
root_agent = None
runner_root = None  # runner 초기화

if greeting_agent and farewell_agent and 'get_weather' in globals():
    # 조율 역할을 담당할 루트 에이전트에는 성능이 뛰어난 Gemini 모델을 사용해봅시다.
    root_agent_model = MODEL_GEMINI_2_0_FLASH

    weather_agent_team = Agent(
        name="weather_agent_42",  # 새로운 버전 이름
        model=root_agent_model,
        description="메인 에이전트: 날씨 처리, 인사/작별 위임, 입력 키워드 검사 기능 포함",
        instruction="당신은 메인 날씨 에이전트입니다. 'get_weather_stateful' 도구를 사용해 날씨 정보를 제공하세요. "
                    "간단한 인사는 'greeting_agent'에게, 작별 인사는 'farewell_agent'에게 위임하세요. "
                    "날씨 요청, 인사, 작별 인사만 처리하세요.",
        tools=[get_weather_stateful, set_temperature_unit],  # 상태기반 stateful 함수로 변경 
        sub_agents=[greeting_agent, farewell_agent],  # 하위 에이전트를 연결합니다!
        output_key="last_weather_report", # <<< 에이전트의 최종 대답 자동 저장
        before_model_callback=block_keyword_guardrail,
        before_tool_callback=block_paris_tool_guardrail,
    )
    print(f"✅ Root Agent '{weather_agent_team.name}' created using model '{root_agent_model}' with sub-agents: {[sa.name for sa in weather_agent_team.sub_agents]}")

else:
    print("❌ Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
    if not greeting_agent: print(" - Greeting Agent is missing.")
    if not farewell_agent: print(" - Farewell Agent is missing.")
    if 'get_weather' not in globals(): print(" - get_weather function is missing.")



# root_agent 또는 weather_agent_team 중 어떤걸 쓰고있는지 체크 사실 의미없음. 지금은 weather_agent_team만 사용하기 때문
# 루트 에이전트 변수가 존재하는지 확인한 후 대화 함수(conversation function)를 정의하세요.
root_agent_var_name = 'root_agent' # Step 3가이드의 기본 이름
if 'weather_agent_team' in globals(): # 이 이름이 대신 사용되었는지 확인
    root_agent_var_name = 'weather_agent_team'
elif 'root_agent' not in globals():
    print("⚠️ Root agent ('root_agent' or 'weather_agent_team') not found. Cannot define run_team_conversation.")
    # 코드 블록이 어쨌든 실행될 경우 NameError를 방지하기 위해 더미 값을 할당하세요.
    root_agent = None

if root_agent_var_name in globals() and globals()[root_agent_var_name]:
    print("\n--- Testing Agent Team Delegation ---")
    # InMemorySessionService는 이 튜토리얼에서 사용하는 간단한 비영속성 저장소입니다.
    session_service = InMemorySessionService()

    # 상호작용 컨텍스트를 식별하기 위한 상수를 정의합니다.
    APP_NAME = "weather_tutorial_agent_team"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team" # 단순함을 위해 고정된 세션ID 사용

    # 초기 세션 상태 지정
    initial_state = {
        "user_preference_temperature_unit": "Celsius"
    }

    # 대화가 진행될 특정 세션을 생성합니다.
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state    # << 초기상태 설정
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    retrieved_session = session_service.get_session(app_name=APP_NAME,
                                                         user_id=USER_ID,
                                                         session_id = SESSION_ID)
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")

    # --- 실제 루트 에이전트 객체 가져오기 ---
    # 확인된 변수 이름을 사용하세요
    actual_root_agent = globals()[root_agent_var_name]

    # 이 에이전트 팀 테스트를 위한 전용 runner를 생성합니다
    runner_agent_team = Runner(
        agent=actual_root_agent, # 루트 에이전트 객체 사용
        app_name=APP_NAME,       # 특정한 앱 이름 사용
        session_service=session_service # 특정한 세션 서비스 사용
        )
    # 실제 루트 에이전트의 이름을 출력하도록 print 문을 수정했습니다
    print(f"Runner created for agent '{actual_root_agent.name}'.")

