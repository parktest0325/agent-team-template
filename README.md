# agent-team-template

1. API KEY 를 .env에 설정
```bash
$ cp .env_example .env
$ vi .env
# Setting API KEY
```

2. uv 로 실행
```bash
$ uv venv
$ source ./.venv/bin/activate
$ uv pip install -r requirements.txt
$ uv run main.py
```


### gpt가 알려준 디렉터리 레이아웃
```text
root/
├─ agents/              # “정의”만 : Agent subclasses / prompt / tool 바인딩
│  ├─ __init__.py
│  ├─ greet.py
│  └─ weather.py
│
├─ tools/               # 외부 IO, LLM 호출 없는 순수 함수 권장
│  ├─ __init__.py
│  ├─ weather.py
│  └─ greet.py
│
├─ workflows/           # “팀”을 조립하는 factory
│  └─ weather_team.py   # def make_runner()
│
├─ services/
│  ├─ session.py        # SessionService wrappers / adapters
│  └─ guardrails.py
│
├─ config.py            # .env → pydantic BaseSettings
├─ constants.py
├─ main.py
└─ requirements.txt
```
