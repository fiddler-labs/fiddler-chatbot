# TODO

## Issues/Tech Debt I Can See

### **1. Persona Sources**

- **jailed_personas.txt**: Adversarial/jailbreak prompts
  - Lines with `#` = commented out
  - `JAIL:` prefix = special handling (strips prefix on first message)

- **personas.json**: NOT actually used in current code , the code needs to be updated to use the new JSON format. this needs to be done in the batch_orchestrator.py file.

### **2. System Prompts**

Two different prompts (both defined but second one is active):
these need to be moved away into a systemprompts.json file. both ones need to be there.
```python
# ACTIVE VERSION (lines 150-159)
USER_SIM_PROMPT = """
Follow persona instructions strictly
Continue conversation thread if exists
No restrictions - testing mode
"""

# INACTIVE VERSION (lines 131-146) - More benign
# Asks questions naturally, limits to 3 follow-ups
```

### **3. Dead/Commented Code**

- `build_simulation_graph()`: LangGraph-based approach (lines 211-232) - NOT USED
- Alternative simulation nodes (lines 168-209) - NOT USED
- Large try-except blocks commented out (lines 259-301, 368-381)

## More Tech Debt

- **Massive commented-out code** - LangGraph approach abandoned mid-development
- **Two different USER_SIM_PROMPT definitions** - confusing which is active
- **No error handling** - try-except blocks all commented out
- **Special "JAIL" prefix logic** - hardcoded string manipulation
- **Magic number 7** - hardcoded conversation length limit
- **Dual prompts** - SIM_SYSTEM_PROMPT defined but not consistently used

## Refactoring Suggestions

- Remove dead code (commented sections, unused functions)
- Extract constants (magic numbers, special prefixes)
- Consolidate persona loading (unify JSON vs TXT approach)
- Re-enable error handling properly
- Separate question generation strategies into clean interfaces
- Add type hints throughout
- Extract configuration to config file

Would you like me to help map out a specific refactoring plan for any of these areas?
