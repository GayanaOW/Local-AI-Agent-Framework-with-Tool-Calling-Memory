import inspect
from typing import Callable, Any, Dict, List
from pydantic import TypeAdapter

class Tool:
    """Wraps a Python function along with its generated JSON schema for Ollama."""
    
    def __init__(self, func: Callable, name: str, description: str, parameters: Dict[str, Any]):
        self.func = func
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_ollama_schema(self) -> Dict[str, Any]:
        """Formats the tool into the exact schema Ollama expects."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    def execute(self, **kwargs) -> Any:
        """Executes the wrapped function with provided arguments."""
        try:
            return self.func(**kwargs)
        except Exception as e:
            return f"Tool Execution Error ({self.name}): {str(e)}"


class ToolRegistry:
    """Manages available tools and generates schemas for LLM tool calling."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, func: Callable = None, *, name: str = None, description: str = None):
        """
        Decorator to register a function as a tool.
        Auto-extracts function signature and docstrings if not explicitly provided.
        """
        def decorator(f: Callable) -> Callable:
            tool_name = name or f.__name__
            tool_doc = description or (f.__doc__.strip() if f.__doc__ else "No description provided.")
            
            parameters_schema = self._generate_json_schema(f)
            
            tool_obj = Tool(
                func=f,
                name=tool_name,
                description=tool_doc,
                parameters=parameters_schema
            )
            
            self._tools[tool_name] = tool_obj
            return f

        if func is None:
            return decorator
        return decorator(func)

    def get_tool(self, name: str) -> Tool:
        """Retrieves a registered tool by name."""
        return self._tools.get(name)

    def get_schemas(self) -> List[Dict[str, Any]]:
        """Returns a list of all tool schemas ready to pass to Ollama API."""
        return [tool.to_ollama_schema() for tool in self._tools.values()]

    def _generate_json_schema(self, func: Callable) -> Dict[str, Any]:
        """Inspects function signature and type hints to produce JSON Schema parameters."""
        sig = inspect.signature(func)
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            # Skip *args or **kwargs
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            # Determine type (default to string if no type hint is provided)
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
            
            # Use Pydantic's TypeAdapter to reliably get JSON schema types
            try:
                json_type = TypeAdapter(param_type).json_schema().get("type", "string")
            except Exception:
                json_type = "string"

            properties[param_name] = {
                "type": json_type,
                "description": f"Parameter {param_name}"
            }

            # If parameter has no default value, it's required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }