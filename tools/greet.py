def say_hello(name: str = "there") -> str:
    """간단한 인사말을 제공합니다. 이름이 주어지면 해당 이름으로 인사합니다.

    매개변수:
        name (str, optional): 인사할 사람의 이름. 기본값은 "there"입니다.

    반환값:
        str: 친근한 인사 메시지입니다.
    """

    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"Hello, {name}!"


def say_goodbye() -> str:
    """대화를 마무리하는 간단한 작별 인사 메시지를 제공합니다."""
    print(f"--- Tool: say_goodbye called ---")
    return "안녕히 가세요! 좋은 하루 보내세요."


print("Greeting and Farewell tools defined.")
print(say_hello("앨리스"))
print(say_goodbye())