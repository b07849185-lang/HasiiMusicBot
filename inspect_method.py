
import inspect
from pytgcalls import PyTgCalls

try:
    print(inspect.signature(PyTgCalls.get_participants))
except Exception as e:
    print(f"Error inspecting signature: {e}")
    try:
        help(PyTgCalls.get_participants)
    except Exception as e2:
        print(f"Error inspecting help: {e2}")
