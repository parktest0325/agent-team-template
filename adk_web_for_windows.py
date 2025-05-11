import os, asyncio, uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Windows + subprocess = Proactor 이벤트 루프
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# agent_dir:  root_agent 가 들어 있는 폴더
# session_db_url / allow_origins 은 필요에 따라 지정
AGENT_DIR = os.path.join(os.path.dirname(__file__), ".")
app = get_fast_api_app(
    agent_dir=AGENT_DIR,
    session_db_url="sqlite:///./sessions.db",    # 제거하면 InMemorySessionServce
    allow_origins=["*"],
    web=True,     # ADK 기본 웹 UI도 노출하려면 True
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, loop="asyncio")