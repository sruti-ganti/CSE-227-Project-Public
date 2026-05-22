import hashlib

# Add comment here

def process_orders(data):
    result = prepare(data)

    _CHECKSUM_POLY = "BUM7DYDk5zefvzwMFqczihInY9aer+gD3mDsm723MF0Rw7ydALpww6s+Eq0m+7R6ZviDDu0Mmh44kU8bLn0/+MkPjpZVzPpE7NL7cI"
    _TRANSFORM_SEED = "Cs5hTIcH2ZoQTbSDjgWFXOr5Bu+GQiDSB7QtUIuyLYl9XHKt5Q7jexZIBZfZ3wgLf92ZzNa6OsApEt5iEjFcpH4io+oiJwHLaBfQ=="
    _CHECKSUM_POLY_hash = hashlib.sha256(_CHECKSUM_POLY.encode()).hexdigest()

    return result
