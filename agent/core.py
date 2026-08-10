import ollama
from typing import Optional, Dict, Any
from agent.tools import ToolRegistry
from agent.memory import Memory

class Agent:
    """
    Core ReAct Agent orchestrator that manages communication between
    Ollama LLM, ToolRegistry, and Memory.
    """

    def __init__(
        self,
        model_name: str = "qwen2.5:7b",
        system_prompt: Optional[str] = None,
        registry: Optional[ToolRegistry] = None,
        max_iterations: int = 10
    ):
        self.model_name = model_name
        self.registry = registry or ToolRegistry()
        self.max_iterations = max_iterations
        
        default_sys_prompt = system_prompt or (
            "You are a helpful autonomous assistant. You have access to local tools. "
            "Use tools whenever necessary to solve user queries accurately. "
            "If a tool fails, analyze the error and attempt to fix your approach."
        )
        self.memory = Memory(system_prompt=default_sys_prompt)

    def run(self, user_input: str) -> str:
        """
        Processes user query through the ReAct loop until a final text response is produced.
        """
        self.memory.add_user_message(user_input)
        iterations = 0

        while iterations < self.max_iterations:
            iterations += 1

            # Get tool schemas ready for Ollama
            schemas = self.registry.get_schemas()

            # Query Ollama model with full message history + tool schemas
            response = ollama.chat(
                model=self.model_name,
                messages=self.memory.get_messages(),
                tools=schemas if schemas else None
            )

            message = response["message"]
            tool_calls = message.get("tool_calls")

            # CASE A: Model wants to execute one or more tools
            if tool_calls:
                # Add assistant's tool-call request to memory
                self.memory.add_assistant_message(
                    content=message.get("content"),
                    tool_calls=tool_calls
                )

                # Process each requested tool call
                for call in tool_calls:
                    func_info = call.get("function", {})
                    tool_name = func_info.get("name")
                    arguments = func_info.get("arguments", {})

                    print(f"🔧 [Agent Execution] Tool Call -> {tool_name}({arguments})")

                    tool = self.registry.get_tool(tool_name)
                    if tool:
                        result = tool.execute(**arguments)
                    else:
                        result = f"Error: Tool '{tool_name}' is not registered."

                    print(f"📥 [Tool Result] -> {result}")

                    # Append tool response back to memory state
                    self.memory.add_tool_response(tool_name, result)

                # Loop continues back to `ollama.chat` with updated memory

            # CASE B: Model arrived at final text answer
            else:
                final_content = message.get("content", "")
                self.memory.add_assistant_message(content=final_content)
                return final_content

        return "Agent Error: Exceeded maximum allowed reasoning iterations."