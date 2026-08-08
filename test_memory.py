from agent.memory import Memory

if __name__ == "__main__":
    mem = Memory(system_prompt="You are a helpful coding assistant.")
    
    mem.add_user_message("What is 10 + 25?")
    mem.add_assistant_message(
        content=None,
        tool_calls=[{"function": {"name": "calculate_sum", "arguments": {"a": 10, "b": 25}}}]
    )
    mem.add_tool_response("calculate_sum", 35)
    mem.add_assistant_message("10 + 25 equals 35.")

    print("--- Formatted Message History ---")
    import json
    print(json.dumps(mem.get_messages(), indent=2))