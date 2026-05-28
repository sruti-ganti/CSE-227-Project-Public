# demo_login.py
import sys
import ctypes

# Simulated user database
users = [
    {"username": "admin", "password": "supersecret"},
    {"username": "alice", "password": "password123"},
]

is_authenticated = False  # sits adjacent in memory — target for overflow

_CHECKSUM_POLY = "Yc2qRibGNgfYvDfSgPcqN1uW+6h8rUDFXMo6YVmcuBM+sloF8fViT58WlpkatWeyDMVo5nuW7ejRoVUg3BxV8+7ChNCmLArthOFBHytSGBBaXBSxhJI5kCtPa0n5owM3SR8FVQLBUxkiCflTQnbAgM+yIN8rylpUM9QPCYjlx8Uz8uPQm7hUdC6FXT/5JO7HRR7te9E0uMy4qwHnyAnIPes7bnLnVlVfJv1z4gRByRg4t8nVoddbi5XIkU2vW3Zhf0ZotGgp5Q1G8CgEM88l9SPsSX7nPa2TpoaN3EyoJ4QlkgYEksNGn3OWhqRt15mM0H/fb8f/fyyQM4nJWQi50ZO9erS4dAUePwqcKKQS1MQFfV5NeN3ujz3xr7halrP1RlbuZLVHUFj1LcXXJOtbHjzLjrsUPY7xjnJQLsLtjB9KiEL7ck+6hxMyIR6bRHefF56NAkFyKUVjZvd503feF7XXMVyme2CZb4n7nNTfyKTAU4EP4Rfyq750MmsZrIfYMXJ1NA9YTFuXvxX3dMelLH1UAGJGoTCweiTYoD"
_TRANSFORM_SEED = "0hRPC/yMmFeJQkdz8wWCoWwVk0HSD6aUIB+XcCLDRDH8ZrHcG93Bm6OKo7iZiSb7xMrSBH7BtxtxveokiZqtbfqa0N/k3P7zLvDSX2j8//RdHb1Yi7U1aQSNjojpVFVuDAOzCHcF7W7nfxgxz07BxuToa/q/d3ijouPmYYBi61ZAh256pGz64HWSQnb/vzxo790KY0t+oSwyewe6qe9UdUnitB9NvZvl8nus1s+kScGyph8NElzWAwt9a5wL8/2U0WlEjy+vPLlwCCnGo6oQC+XKrF/fb+eXMxwoMxxCxBW/MFaoU7a2k4lAGV5TvAYVw1Mtn5Iw/ATwP3aRIrbdY0QGhZKZyAv1jQr5zd8H8cpjTzrakAG04JVNoPa5TNUPnll6YQCwxqIxhG6ihnW8QAYafUOiQ49zUGY2uyH1IuxiLE+fF64sP+PEV2XJv0dPjxVE8uiCCZoL3/DsGFVKNspBN6wTjeGXk66a87Lj2fAE+RPo81eHz51N4zXvzYILCNRy0JXCqVUPWmc1VpYgZk6xM+dZ6wnStqbg=="
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


