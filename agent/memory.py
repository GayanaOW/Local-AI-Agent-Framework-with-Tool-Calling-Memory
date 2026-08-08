from typing import List, Dict, Any, Optional

class Memory:
    """
    Manages the conversation state and message history formatted for Ollama tool calling.
    """

    def __init__(self, system_prompt: Optional[str] = None):
        self.messages: List[Dict[str, Any]] = []
        if system_prompt:
            self.set_system_prompt(system_prompt)

    def set_system_prompt(self, prompt: str):
        """Sets or replaces the initial system prompt."""
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = prompt
        else:
            self.messages.insert(0, {"role": "system", "content": prompt})

    def add_user_message(self, content: str):
        """Adds a user input message."""
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: Optional[str] = None, tool_calls: Optional[List[Dict[str, Any]]] = None):
        """
        Adds an assistant response. Can include text content, tool calls, or both.
        """
        message: Dict[str, Any] = {"role": "assistant"}
        if content:
            message["content"] = content
        if tool_calls:
            message["tool_calls"] = tool_calls
        self.messages.append(message)

    def add_tool_response(self, tool_name: str, response_content: Any):
        """
        Adds a tool execution result to the history.
        Ollama expects tool results as role 'tool'.
        """
        self.messages.append({
            "role": "tool",
            "content": str(response_content),
            "name": tool_name
        })

    def get_messages(self) -> List[Dict[str, Any]]:
        """Returns full formatted message history."""
        return self.messages

    def clear(self, keep_system: bool = True):
        """Clears memory history."""
        if keep_system and self.messages and self.messages[0]["role"] == "system":
            system_msg = self.messages[0]
            self.messages = [system_msg]
        else:
            self.messages = []