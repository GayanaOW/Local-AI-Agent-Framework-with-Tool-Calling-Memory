from agent.core import Agent
from agent.tools import ToolRegistry

# Initialize registry
registry = ToolRegistry()

# Define real sample tools
@registry.register
def calculate_sum(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b

@registry.register
def multiply_numbers(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b

if __name__ == "__main__":
    # Change model_name to whichever tool-calling model you pulled in Ollama
    agent = Agent(model_name="qwen2.5:7b", registry=registry)

    print("🤖 Agent Framework initialized. Ask a question (type 'exit' to quit):\n")
    
    while True:
        try:
            user_input = input("User > ")
            if user_input.strip().lower() in ["exit", "quit"]:
                break

            response = agent.run(user_input)
            print(f"\nAssistant > {response}\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}\n")