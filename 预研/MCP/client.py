import asyncio
from fastmcp import Client
from fastmcp.client import StreamableHttpTransport, SSETransport


async def main():
    # client = Client("http://10.185.212.200:8192/mcp")
    client = Client(transport=StreamableHttpTransport(url="http://ww.ee", sse_read_timeout=5), timeout=5)
    # Connection is established here
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        if any(tool.name == "hello" for tool in tools):
            result = await client.call_tool("hello", {"name": "World"})
            print(f"Greet result: {result}")

        # Connection is closed automatically here
        print(f"Client connected: {client.is_connected()}")

if __name__ == "__main__":
    asyncio.run(main())