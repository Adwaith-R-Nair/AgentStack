from ddgs import DDGS

from agentstack.tools.base_tool import BaseTool


class WebSearchTool(BaseTool):
    """
    Tool for searching the web using DuckDuckGo.
    """

    name = "web_search"
    description = "Searches the web for information."

    def run(self, input: str) -> str:

        try:
            results = []

            with DDGS() as ddgs:
                for r in ddgs.text(input, max_results=3):
                    results.append(f"{r['title']} — {r['body']}")

            if not results:
                return "No results found."

            return "\n".join(results)

        except Exception as e:
            return f"Search error: {str(e)}"