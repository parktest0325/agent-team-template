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

