# agent-team-template
google-adk 의 tutorial을 기준으로 파일을 나눠둔 샘플 프로젝트입니다.       
이 프로젝트를 클론하여 원하는 프로젝트를 구현할 수 있습니다.        
This is a sample project structured based on the google-adk tutorial.       
You can clone this repository to build your own custom project.    

## TODO
- [x] MCP 연동  
      Integrated with MCP
- [ ] 결과가 나올때까지 무한히 반복하는 구조 구현     
      Implements a loop that runs until the desired result is achieved
- [ ] Agent와 통신할 인터페이스를 슬랙봇으로 구현    
      Implements a Slack bot as the interface for communicating with the agent


<br>


## MCP 세팅
예시는 옵시디언
![image](https://github.com/user-attachments/assets/8c5104dd-c0da-4a50-a66f-d0b54f3bed36)



<br>

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

#### 결과
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

<br>

### adk web으로 실행
```bash
$ adk web
# using browser. access at http://localhost:8000

# if windows
$ uv run adk_web_for_windows.py
# using browser. access at http://localhost:8000
```

#### 결과

![image](https://github.com/user-attachments/assets/d6db62b2-01f6-4dc8-81a9-c10b1b1f04bf)



<br>

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
