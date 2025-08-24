# agent/run.py
"""
Entrypoint to run the AuditorAgent defined in auditor.yaml.
"""

import yaml
from portia import Portia, Config, DefaultToolRegistry

if __name__ == "__main__":
    # Load workflow YAML
    with open("agent/auditor.yaml", "r", encoding="utf-8") as f:

        yaml_data = yaml.safe_load(f)

    # Create Portia agent
    config = Config(model="gpt-4o", temperature=0.2)  # You can customize this
    tools = DefaultToolRegistry(config=config)
    portia = Portia(yaml_data, config=config, tools=tools)

    # === Example 1: User Input Check ===
    user_input = "Contact me at john@acme.com. My token is sk_1234567890abcdefghijklmnop."
    result_input = portia.run({"doc": user_input, "mode": "input"})
    print("\n=== User Input Check ===")
    print("Original:", user_input)
    print("Verdict:", result_input["verdict"])
    print("Cleaned:", result_input["clean_doc"])

    # === Example 2: AI Output Check ===
    ai_output = "The secret key for the system is sk_abcdef123456. Also, people from XYZ group are bad."
    result_output = portia.run({"doc": ai_output, "mode": "output"})
    print("\n=== AI Output Check ===")
    print("Original:", ai_output)
    print("Verdict:", result_output["verdict"])
    print("Cleaned:", result_output["clean_doc"])
