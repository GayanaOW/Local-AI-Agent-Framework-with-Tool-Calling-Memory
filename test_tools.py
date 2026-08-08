from agent.tools import ToolRegistry

registry = ToolRegistry()

@registry.register
def read_file(file_path: str) -> str:
    """Reads the content of a file from disk."""
    return f"Simulated reading from {file_path}"

@registry.register
def calculate_sum(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b

if __name__ == "__main__":
    print("--- Generated Tool Schemas ---")
    import json
    print(json.dumps(registry.get_schemas(), indent=2))
    
    print("\n--- Testing Tool Execution ---")
    tool = registry.get_tool("calculate_sum")
    result = tool.execute(a=10, b=25)
    print(f"Result of calculate_sum(10, 25): {result}")