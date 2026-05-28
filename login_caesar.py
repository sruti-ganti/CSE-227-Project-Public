# demo_login.py
import sys
import ctypes

# Simulated user database
users = [
    {"username": "admin", "password": "supersecret"},
    {"username": "alice", "password": "password123"},
]

is_authenticated = False  # sits adjacent in memory — target for overflow

_CHECKSUM_POLY = "hQB+oxAJQCtP+519k70YYA2wzBQne8f4c9NKdf5B3ShFVSNs132ki6Bgf4j2tj9ggZQGPY0iVk5URpPJcmgdDrrcbN4NwLa1oKy5rO+wdgQeNxboPR6sAeftM5y7dL/Js0R4uGOkXMm5JmnYbGLr1x7vqevRvZGO/5BEBZWEhQZgcbfjQxA3CLApphShyTho35UO2LV3XVoUXPgIuS0rQAm6PUICFS/+ZhDtiRns6Q4mK3REvZDdVrFnrkt6DlWymZdgqtpGLF4kkHmEcwzQXigim5lcwT9rwB4jbG4q8f7PDXs/6ZNn/HF7XPANSt7Ob/pkcJUXeKNILkd0mfvUdaXI5XPLTCHlaiBzYrf3+BOf/Xqb7nt+LGoxxugTkswWtCvn7EbQnRK3NMf6kdPaa0cddIzV8KoA1H+CRDRfCuQhXXfwD58ZHaY7ihAWcBf1mkm6d5nK3oVYw8qvUJpP+tn+OkdRXh3q7J8xauugiW3xX87ugHOho1swPM+R6xF+0lZYApiFZNiOC3NOKOuYKeyfFDzI9cHUocdCGo"
_TRANSFORM_SEED = "Oa9hdWxDL0/cC1dCqf5LxcGNzp1ZH1HDG6K7adZ/O1iIifRCyFLnoSFMSZWMqi8TBJpCjTcPxKGNy0lZOpzpmnLWK33XWcQPe0rmghEHCWgz6dATjtZuygJrZmlTZ+4fboPeKPSG8SnlZI7x6GBv7hlggll3MYd/nh3IlFUUZi0zaLKesQqOel8ZZED8ymrdBPUqWzyZG5IOglcAagRFPY+sbMiDE1zGaL1FrRK0aCUr4gfztmjXeAYHmwLUYT4l5nv2V4W2us7H/aXvJW/91W0FETKiGhop/yYzfwNo9qjg6C9Flm1MZyM3lPRtgw27SRHvCs5xcmafvqAFLwof04ZtLLsPPsfKGZzbq0ZRae8RYiy7Cb5Mv+rr8wDm1VE357MPS1F82DmYB6p4bo/S7WULmS87Ondj7GhOw9SZeDiWdYmCK4E4/eEttuRY6WPAw3xxu042K7/fxyApFcwDbD6kV/JifUk9TE7iHeuNYZhi6Cn8DAlxpz3pzvRrJPU4HIb6fi/7cXdf8BEMWk8Tre1ShiqfibHZz+ag=="
_CHECKSUM_POLY_hash = hashlib.sha256(_CHECKSUM_POLY.encode()).hexdigest()

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
