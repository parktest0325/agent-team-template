from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types # 응답을 생성하기 위해 필요
from typing import Optional

def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    가장 최근 사용자의 메시지에 'BLOCK'이 포함되어 있는지 검사합니다.
    포함되어 있다면 LLM 호출을 차단하고 미리 정의된 LlmResponse를 반환합니다.
    포함되어 있지 않으면 None을 반환하여 다음 단계로 진행하게 합니다.
    """
    agent_name = callback_context.agent_name # 모델 호출이 가로채진 에이전트의 이름을 가져옵니다
    print(f"--- Callback: block_keyword_guardrail running for agent: {agent_name} ---")

    # 요청 기록에서 최신 사용자 메시지의 텍스트를 추출합니다
    last_user_message_text = ""
    if llm_request.contents:
        # 역할이 'user'인 가장 최근 메시지를 찾습니다
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                # 간단하게 처리하기 위해 텍스트가 첫 번째 부분에 있다고 가정합니다
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break # 마지막 사용자 메시지 텍스트를 찾았습니다

    print(f"--- Callback: Inspecting last user message: '{last_user_message_text[:100]}...' ---") # 첫 100개 문제 출력

    # --- 가드레일 로직 ---
    keyword_to_block = "BLOCK"
    if keyword_to_block in last_user_message_text.upper(): # 대소문자 구분 없이 체크
        print(f"--- Callback: Found '{keyword_to_block}'. Blocking LLM call! ---")
        # 선택적으로, 차단 이벤트를 기록하기 위해 상태에 플래그를 설정할 수 있습니다.
        callback_context.state["guardrail_block_keyword_triggered"] = True
        print(f"--- Callback: Set state 'guardrail_block_keyword_triggered': True ---")

        # 흐름을 중단하고 이 응답을 대신 보내기 위해 LlmResponse를 생성하여 반환합니다
        return LlmResponse(
            content=types.Content(
                role="model", # 에이전트의 관점에서 보낸 응답처럼 가장합니다
                parts=[types.Part(text=f"이 요청에는 차단된 키워드 '{keyword_to_block}'가 포함되어 있어 처리할 수 없습니다.")],
            )
            # 참고: 필요하다면 여기에서 error_message 필드를 설정할 수도 있습니다
        )
    else:
        # 키워드가 발견되지 않았으므로 요청이 LLM으로 전달되도록 허용합니다
        print(f"--- Callback: Keyword not found. Allowing LLM call for {agent_name}. ---")
        return None # None을 반환하면 ADK가 정상적으로 계속 진행하라는 신호를 보냅니다

print("✅ block_keyword_guardrail function defined.")


# @title 1. before_tool_callback 가드레일 정의하기

# 필요한 import가 준비되어 있는지 확인하세요
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from typing import Optional, Dict, Any # 타입 힌팅

def block_paris_tool_guardrail(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    """
    'get_weather_stateful' 도구가 'Paris'에 대해 호출되었는지 확인합니다.
    해당하는 경우, 도구 실행을 차단하고 특정 오류 딕셔너리를 반환합니다.
    그렇지 않으면 None을 반환하여 도구 호출이 계속 진행되도록 허용합니다.
    """
    tool_name = tool.name
    agent_name = tool_context.agent_name # 도구 호출을 시도하는 에이전트
    print(f"--- Callback: block_paris_tool_guardrail running for tool '{tool_name}' in agent '{agent_name}' ---")
    print(f"--- Callback: Inspecting args: {args} ---")

    # --- 가드레일 로직 ---
    target_tool_name = "get_weather_stateful" # FunctionTool에서 사용하는 함수 이름과 일치시킵니다
    blocked_city = "paris"

    # 올바른 도구인지, 그리고 `city` 인자가 차단 대상 도시와 일치하는지 확인합니다
    if tool_name == target_tool_name:
        city_argument = args.get("city", "") # 안전하게 `'city'` 인자를 가져옵니다
        if city_argument and city_argument.lower() == blocked_city:
            print(f"--- Callback: Detected blocked city '{city_argument}'. Blocking tool execution! ---")
            # 선택적으로 상태를 업데이트합니다
            tool_context.state["guardrail_tool_block_triggered"] = True
            print(f"--- Callback: Set state 'guardrail_tool_block_triggered': True ---")

            # 오류에 대한 도구의 예상 출력 형식과 일치하는 딕셔너리를 반환합니다
            # 이 딕셔너리는 도구의 결과로 처리되며, 실제 도구 실행은 건너뜁니다
            return {
                "status": "error",
                "error_message": f"정책 제한: '{city_argument.capitalize()}'에 대한 날씨 조회는 현재 도구 가드레일에 의해 비활성화되어 있습니다."
            }
        else:
             print(f"--- Callback: City '{city_argument}' is allowed for tool '{tool_name}'. ---")
    else:
        print(f"--- Callback: Tool '{tool_name}' is not the target tool. Allowing. ---")


    # 위의 검사에서 딕셔너리를 반환하지 않았다면, 도구 실행을 허용합니다
    print(f"--- Callback: Allowing tool '{tool_name}' to proceed. ---")
    return None # `None`을 반환하면 실제 도구 함수가 실행됩니다

print("✅ block_paris_tool_guardrail function defined.")
