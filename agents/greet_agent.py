from tools.greet import *
from constant import MODEL_GEMINI_2_0_FLASH
from google.adk.agents import Agent

def build_greet_agent() -> Agent:
    return Agent(
        # 단순한 작업에는 더 간단하거나 저렴한 모델을 사용할 수도 있습니다.
        model=MODEL_GEMINI_2_0_FLASH,
        name="greeting_agent",
        instruction="당신은 인사 전용 에이전트입니다. 당신의 유일한 역할은 사용자에게 친근하게 인사하는 것입니다. "
                    "'say_hello' 도구를 사용해 인사말을 생성하세요. "
                    "사용자가 이름을 제공하면 해당 이름을 도구에 전달해야 합니다. "
                    "그 외의 대화나 작업은 수행하지 마세요.",
        description="'say_hello' 도구를 이용해 간단한 인사 요청을 처리합니다.",  # 위임 시 중요한 설명입니다.
        tools=[say_hello],
    )

def build_farewell_agent() -> Agent:
    return Agent(
        # 같은 모델 또는 다른 모델을 사용할 수 있습니다.
        model=MODEL_GEMINI_2_0_FLASH,
        name="farewell_agent",
        instruction="당신은 작별 인사 전용 에이전트입니다. 당신의 유일한 역할은 정중한 작별 인사를 제공하는 것입니다. "
                    "사용자가 대화를 끝내려는 의사를 보일 때(예: 'bye', 'goodbye', 'thanks bye', 'see you', '잘가', '안녕.' 등의 표현 사용 시) "
                    "'say_goodbye' 도구를 사용하세요. "
                    "그 외의 작업은 수행하지 마세요.",
        description="'say_goodbye' 도구를 이용해 간단한 작별 인사 요청을 처리합니다.",  # 위임 시 중요한 설명입니다.
        tools=[say_goodbye],
    )