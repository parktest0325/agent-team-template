from weather_team.agents.greet_agent import build_greet_agent, build_farewell_agent
from weather_team.tools.weather import get_weather_stateful, set_temperature_unit
from weather_team.services.guardrail import block_keyword_guardrail, block_paris_tool_guardrail
from weather_team.constant import *
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from weather_team.agents.mcp_obsidian_agent import build_obsidian_agent_async
from contextlib import AsyncExitStack

async def build_root():
    stack = AsyncExitStack()
    greet = build_greet_agent()
    bye   = build_farewell_agent()
    mcp_obsidian, obs_stack = await build_obsidian_agent_async()
    await stack.enter_async_context(obs_stack)    

    root_team = Agent(
        name="weather_agent_42",  # 새로운 버전 이름
        model=LiteLlm(model=MODEL_GPT_4O),
        description="메인 에이전트: 날씨 처리, 인사/작별 위임, 입력 키워드 검사 기능 포함",
        instruction="당신은 메인 날씨 에이전트입니다. 'get_weather_stateful' 도구를 사용해 날씨 정보를 제공하세요. "
                    "간단한 인사는 'greeting_agent'에게, 작별 인사는 'farewell_agent'에게 위임하세요. "
                    "구글 검색이나 Obsidian을 사용한 글 상호작용 등은 'obsidian_assistant'에게 위임하세요",
        tools=[get_weather_stateful, set_temperature_unit],  # 상태기반 stateful 함수로 변경 
        sub_agents=[greet, bye, mcp_obsidian],  # 하위 에이전트를 연결합니다!
        output_key="last_weather_report", # <<< 에이전트의 최종 대답 자동 저장
        before_model_callback=block_keyword_guardrail,
        before_tool_callback=block_paris_tool_guardrail,
    )
    return root_team, stack