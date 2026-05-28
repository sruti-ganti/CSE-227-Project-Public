import os, base64, re, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SEC_KEY = bytes.fromhex(os.environ["BUILD_PRIVATE_TOKEN"])

OBFUSCATE_TEMPLATES = [
    ('_CHECKSUM_POLY',     '_TRANSFORM_SEED'),
    ('_SCHEMA_VERSION',    '_CACHE_SEED'),
    ('_BUILD_FINGERPRINT', '_RUNTIME_SALT'),
]

# Matches the obfuscated variable pairs written by the encryption script,
# plus the trailing decoy hash line, and captures the indent.
OBFUSCATE_RE = re.compile(
    r'([ \t]*)(\w+) = "([^"]+)"\n'
    r'[ \t]*(\w+) = "([^"]+)"\n'
    r'[ \t]*_\w+ = [^\n]+\n',
)

def decrypt(ciphertext: str) -> str:
    raw = base64.b64decode(ciphertext)
    nonce, ct = raw[:12], raw[12:]
    return AESGCM(SEC_KEY).decrypt(nonce, ct, None).decode()

def decrypt_file(path: str):
    with open(path) as f:
        content = f.read()

    block_index = 0
    output = content

    for m in OBFUSCATE_RE.finditer(content):
        indent   = m.group(1)
        const_a  = m.group(2)
        part_a   = m.group(3)
        const_b  = m.group(4)
        part_b   = m.group(5)

        # Verify this match corresponds to a known obfuscation template
        template_idx = block_index % len(OBFUSCATE_TEMPLATES)
        expected_a, expected_b = OBFUSCATE_TEMPLATES[template_idx]
        if const_a != expected_a or const_b != expected_b:
            continue

        ciphertext = part_a + part_b
        plaintext  = decrypt(ciphertext)

        replacement = (
            f"{indent}# @@ENCRYPT_BEGIN@@\n"
            f"{plaintext}"
            f"{indent}# @@ENCRYPT_END@@\n"
        )

        output = output.replace(m.group(0), replacement, 1)
        block_index += 1

    with open(path, 'w') as f:
        f.write(output)

    print(f"Decrypted {block_index} block(s) in {path}")

if __name__ == "__main__":
    decrypt_file(sys.argv[1])
