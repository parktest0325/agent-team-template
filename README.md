# agent-team-template

## 실행하기
### 직접 실행
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

<br>

### adk web으로 실행
```bash
$ adk web
# using browser. access at http://localhost:8000
```



<br>

### 결과
```text
➜ hi 나는 dongkim 이야
Hello, dongkim!

➜ Paris의 ㅣ날씨를 알려줘
죄송합니다. 정책 제한으로 인해 현재 Paris의 날씨를 조회할 수 없습니다. 다른 도시를 알려주시겠습니까?

➜ London의 날씨를 알려줘
현재 London의 날씨는 15°C이며 흐립니다.

➜ 화씨로 알고싶은데
온도 단위를 화씨로 변경했습니다. 다음 질문부터는 화씨로 답변해 드리겠습니다.

➜ Tokyo의 날씨를알려줘
현재 Tokyo의 날씨는 가벼운 비가 내리고 있으며, 온도는 64°F입니다.

➜ Paris의 날씨를 알려줘
죄송합니다. 정책 제한으로 인해 현재 Paris의 날씨를 조회할 수 없습니다. 다른 도시를 알려주시겠습니까?

➜ bye
안녕히 가세요! 좋은 하루 보내세요.

➜ exit
```



## 디렉터리 레이아웃
```text
root/
├─ agents/              # “정의”만 : Agent subclasses / prompt / tool 바인딩
│  ├─ greet_agent.py
│  └─ root_agent.py
│
├─ tools/               # 외부 IO, LLM 호출 없는 순수 함수 권장
│  ├─ weather.py
│  └─ greet.py
│
├─ workflows/           # “팀”을 조립하는 factory
│  └─ weather_team.py   # make_runner()
│
├─ services/
│  ├─ session.py        # SessionService wrappers / adapters
│  └─ guardrails.py
│
├─ config.py            # .env load
├─ constants.py
├─ main.py
└─ requirements.txt
```
