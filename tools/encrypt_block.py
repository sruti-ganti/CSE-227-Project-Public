# Reference: https://csrc.nist.rip/groups/ST/toolkit/BCM/documents/proposedmodes/gcm/gcm-spec.pdf

import os, base64, re, sys, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SEC_KEY = bytes.fromhex(os.environ["BUILD_PUBLIC_TOKEN"])

MARKER_RE = re.compile(
    r'([ \t]*)# @@ENCRYPT_BEGIN@@\n(.*?)# @@ENCRYPT_END@@\n',
    re.DOTALL
)

OBFUSCATE_TEMPLATES = [
    ('_CHECKSUM_POLY',    '_TRANSFORM_SEED',    'hashlib.sha256({0}.encode()).hexdigest()'),
    ('_SCHEMA_VERSION',   '_CACHE_SEED',        'hashlib.md5({0}.encode()).hexdigest()'),
    ('_BUILD_FINGERPRINT','_RUNTIME_SALT',      'hashlib.sha1({0}.encode()).hexdigest()'),
]

def encrypt(plaintext: str) -> str:
    nonce = os.urandom(12)
    ct = AESGCM(SEC_KEY).encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ct).decode()

def obfuscate(ciphertext: str, indent: str, block_index: int) -> str:
    t = OBFUSCATE_TEMPLATES[block_index % len(OBFUSCATE_TEMPLATES)]
    const_a, const_b = t[0], t[1]
    decoy_expr = t[2]
    mid = len(ciphertext) // 2
    part_a = ciphertext[:mid]
    part_b = ciphertext[mid:]
    decoy = decoy_expr.format(const_a)
    return (
        f"{indent}{const_a} = \"{part_a}\"\n"
        f"{indent}{const_b} = \"{part_b}\"\n"
        f"{indent}_{const_a[1:]}_hash = {decoy}\n"
    )

def encrypt_file(path: str):
    with open(path) as f:
        content = f.read()
    block_index = 0
    def replacer(m):
        nonlocal block_index
        indent = m.group(1)
        block  = m.group(2)
        cipher = encrypt(block)
        result = obfuscate(cipher, indent, block_index)
        block_index += 1
        return result
    result = MARKER_RE.sub(replacer, content)
    with open(path, 'w') as f:
        f.write(result)
    print(f"Encrypted {block_index} block(s) in {path}")

if __name__ == "__main__":
    encrypt_file(sys.argv[1])
