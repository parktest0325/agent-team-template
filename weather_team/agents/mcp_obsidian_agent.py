import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
  """Gets tools from the Obsidian MCP Server."""
  print("Attempting to connect to MCP Obsidian server...")
  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command='uvx', # Command to run the server
          args=[
                "mcp-obsidian",
                ],
          env={
            "OBSIDIAN_API_KEY": os.environ["OBSIDIAN_API_KEY"],
            "OBSIDIAN_HOST": os.environ["OBSIDIAN_HOST"],
          }
      )
  )
  print("MCP Toolset created successfully.")
  return tools, exit_stack

# --- Step 2: Agent Definition ---
async def build_obsidian_agent_async():
    """obsidian MCP + google search 가 장착된 최상위 에이전트"""
    tools, exit_stack = await get_tools_async()
    print(f"Fetched {len(tools)} tools from MCP server.")

    search_tool = LlmAgent(
        model='gemini-2.5-flash-preview-04-17',
        name='google_search_agent',
        instruction="사용자 요청에 맞춰 Google 웹 검색 결과를 제공한다.",
        tools=[google_search], # Provide the MCP tools to the ADK agent
    )

    obsidian_agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17',
        name='obsidian_assistant',
        instruction="사용자가 사용할 수 있는 도구들을 통해 Obsidian과 상호작용할 수 있도록 한다.",
        tools=tools + [AgentTool(agent=search_tool)],
    )
    return obsidian_agent, exit_stack