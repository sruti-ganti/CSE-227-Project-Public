# demo_login.py
import sys
import ctypes

# Simulated user database
users = [
    {"username": "admin", "password": "supersecret"},
    {"username": "alice", "password": "password123"},
]

is_authenticated = False  # sits adjacent in memory — target for overflow

# @@ENCRYPT_BEGIN@@
def check_password(username: str, input_password: str) -> bool:
    global is_authenticated

    # Simulate fixed 16-byte buffer using ctypes
    buffer = ctypes.create_string_buffer(16)

    print(f"[DEBUG] buffer is at:          {ctypes.addressof(buffer):#x}")
    print(f"[DEBUG] is_authenticated is at: {id(is_authenticated):#x}")

    # Simulate strcpy with no bounds check (overflow behavior)
    buffer.raw = input_password.encode()[:16].ljust(16, b'\x00')

    # Overflow simulation: if input > 16 bytes, flip is_authenticated
    if len(input_password) > 16:
        is_authenticated = True  # simulates stack overflow overwriting the flag

    for user in users:
        if user["username"] == username and user["password"] == input_password:
            return True

    return False
# @@ENCRYPT_END@@

def main():
    global is_authenticated

    print("=== Demo Login System ===")
    username = input("Username: ")
    password = input("Password: ")

    if check_password(username, password):
        print(f"\n Login successful! Welcome, {username}.")
    elif is_authenticated:
        # is_authenticated may have been flipped by the overflow simulation
        print("\n Wrong password — but is_authenticated was overwritten!")
        print(" Bypass successful! You're in without valid credentials.")
    else:
        print("\n Login failed.")

if __name__ == "__main__":
    main()


