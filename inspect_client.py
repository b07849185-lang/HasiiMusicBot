
from pyrogram import Client
import inspect

try:
    print("Checking get_group_call_participants:")
    print(inspect.signature(Client.get_group_call_participants))
except Exception as e:
    print(f"Client.get_group_call_participants not found or error: {e}")

try:
    print("\nChecking get_participants:")
    print(inspect.signature(Client.get_participants))
except Exception as e:
    print(f"Client.get_participants not found or error: {e}")
