# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.secrets module
# Generated files: client/anvil/secrets.pyi, server/anvil/secrets.pyi

class SecretError(Exception):
    """Secret access or encryption error."""
    ...

def get_secret(secret_name: str) -> str:
    """Retrieve the named secret."""
    ...

def encrypt_with_key(key_name: str, value: str) -> str:
    """Encrypt a string with a cryptographic key derived from the named secret."""
    ...

def decrypt_with_key(key_name: str, value: str) -> str:
    """Decrypt a string with a cryptographic key derived from the named secret."""
    ...
