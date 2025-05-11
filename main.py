import asyncio
import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

import config

print("Libraries imported.")

from google.genai import types
async def ask(query: str, runner, user_id, session_id):
    # 사용자 메시지를 ADK 형식으로 준비한다.
    content = types.Content(role="user", parts=[types.Part(text=query)])

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                # 처음 부분에 텍스트 응답이 있다고 가정
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # 잠재적인 오류나 에스컬레이션 상황
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message'}"
            # 필요하다면 여기에서 추가적인 확인을 수행하세요 (예: 특정 오류 코드 등).
            break # 최종 응답을 찾으면 이벤트 처리를 중단합니다.
    print(f"{final_response_text}")


from weather_team.workflows.weather_team import make_runner, USER_ID, SESSION_ID
runner = make_runner()

async def loop():
    print("🌤  Weather CLI – type 'exit' to quit")
    while True:
        q = input("➜ ")
        if q.lower() in {"exit", "quit"}:
            break
        await ask(q, runner, USER_ID, SESSION_ID)

        # 질문 한번마다 스테이트 확인
        # final_session = session_service.get_session(app_name=APP_NAME,
        #                         user_id= USER_ID,
        #                         session_id=SESSION_ID)
        # print(f"Full State: {final_session.state}")

if __name__ == "__main__":
    try:
        asyncio.run(loop())
    except Exception as e:
        print(f"An error occurred: {e}")