from agentstack.tools.base_tool import BaseTool


class FileReaderTool(BaseTool):
    """
    Tool for reading file contents from disk.
    """

    name = "file_reader"
    description = "Reads file contents from disk."

    def run(self, input: str) -> str:
        """
        Read the contents of a file.

        Args:
            input (str): Path to the file

        Returns:
            str: File contents
        """

        try:
            with open(input, "r", encoding="utf-8") as f:
                return f.read()

        except Exception as e:
            return f"Error reading file: {str(e)}"