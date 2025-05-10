from agents.greet_agent import greeting_agent, farewell_agent
from tools.weather import get_weather
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
        name="weather_agent_v2",  # 새로운 버전 이름
        model=root_agent_model,
        description="날씨 요청을 처리하고 인사/작별은 전문 하위 에이전트에게 위임하는 메인 조율 에이전트입니다.",
        instruction="당신은 팀을 조율하는 메인 날씨 에이전트입니다. 주된 역할은 날씨 정보를 제공하는 것입니다. "
                    "'get_weather' 도구는 특정한 날씨 요청(예: '런던 날씨 알려줘')에만 사용하세요. "
                    "당신에게는 두 명의 전문 하위 에이전트가 있습니다: "
                    "1. 'greeting_agent': '안녕', '반가워'와 같은 간단한 인사를 처리합니다. 이런 경우 이 에이전트에게 위임하세요. "
                    "2. 'farewell_agent': '잘가', '또 봐'와 같은 작별 인사를 처리합니다. 이런 경우 이 에이전트에게 위임하세요. "
                    "사용자의 요청을 분석하세요. 인사면 'greeting_agent'에게, 작별이면 'farewell_agent'에게 위임하세요. "
                    "날씨 요청이면 직접 'get_weather' 도구로 처리하세요. "
                    "그 외의 경우에는 적절히 응답하거나 처리할 수 없음을 알려주세요.",
        tools=[get_weather],  # 루트 에이전트는 여전히 날씨 요청을 위해 get_weather 도구를 사용합니다.
        sub_agents=[greeting_agent, farewell_agent]  # 하위 에이전트를 연결합니다!
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

    # 대화가 진행될 특정 세션을 생성합니다.
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

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
