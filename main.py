import os
import asyncio
from google.genai import types

import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")

from dotenv import load_dotenv
load_dotenv()


# --- 키 확인 (선택적인 확인) ---
print("API Keys Set:")
print(f"Google API Key set: {'Yes' if os.environ.get('GOOGLE_API_KEY') and os.environ['GOOGLE_API_KEY'] != 'YOUR_GOOGLE_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")
print(f"OpenAI API Key set: {'Yes' if os.environ.get('OPENAI_API_KEY') and os.environ['OPENAI_API_KEY'] != 'YOUR_OPENAI_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")
print(f"Anthropic API Key set: {'Yes' if os.environ.get('ANTHROPIC_API_KEY') and os.environ['ANTHROPIC_API_KEY'] != 'YOUR_ANTHROPIC_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")

print("\nEnvironment configured.")


from google.genai import types
# LLM 이랑 외부 API 같은 도구와의 상호작용은 IO작업인데, 그래서 asyncio로 작업을 효율적으로 블로킹이 되지 않도록 한다.
async def call_agent_async(query: str, runner, user_id, session_id):
    """에이전트에 쿼리를 보내고, 최종 응답을 출력한다."""
    print(f"\n>>> User Query: {query}")

    # 사용자 메시지를 ADK 형식으로 준비한다.
    content = types.Content(role="user", parts=[types.Part(text=query)])

    # 핵심 컨셉: run_async는 에이전트의 로직을 실행하고 Event들을 생성합니다.
    # 최종 답변을 찾기 위해 이벤트들을 반복(iterate)합니다.
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # 아래 줄의 주석을 해제하면 실행 중 발생하는 *모든* 이벤트를 확인할 수 있습니다.
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # 핵심 컨셉: is_final_response()는 해당 턴의 마지막 메시지임을 나타냅니다.
        if event.is_final_response():
            if event.content and event.content.parts:
                # 처음 부분에 텍스트 응답이 있다고 가정
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # 잠재적인 오류나 에스컬레이션 상황
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message'}"
            # 필요하다면 여기에서 추가적인 확인을 수행하세요 (예: 특정 오류 코드 등).
            break # 최종 응답을 찾으면 이벤트 처리를 중단합니다.

    print(f"<<< Agent Response: {final_response_text}")


from agents.root_agent import runner_agent_team, session_service, APP_NAME, USER_ID, SESSION_ID
from agents.gpt4o_agent import gpt_runner, USER_ID_GPT, SESSION_ID_GPT

async def run_conversation():
    while True:
        q = input("Question?")
        await call_agent_async(q,
                            runner=runner_agent_team,
                            user_id=USER_ID,
                            session_id=SESSION_ID)
        # 질문 한번마다 스테이트 확인
        final_session = session_service.get_session(app_name=APP_NAME,
                                user_id= USER_ID,
                                session_id=SESSION_ID)
        print(f"Full State: {final_session.state}")

        # await call_agent_async(query=q,
        #     runner=gpt_runner,
        #     user_id=USER_ID_GPT,
        #     session_id=SESSION_ID_GPT)

if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")