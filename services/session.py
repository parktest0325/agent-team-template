from google.adk.sessions import InMemorySessionService

def create_session_service() -> InMemorySessionService:
    return InMemorySessionService()