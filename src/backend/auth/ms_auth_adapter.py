import base64
import json
from functools import cache

import httpx
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from jwt import PyJWTError

from src.backend.helpers import get_logger

logger = get_logger()


class MSAuthAdapter:
    _instance = None

    def __init__(self, client_id, tenant_id, auth_policy, auth_url):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.policy = auth_policy
        self.base_url = auth_url + "/" + self.tenant_id
        self.issuer = self.base_url + "/v2.0/"
        self.other_issuer = "https://login.microsoftonline.com/" + self.tenant_id + "/v2.0"
        self.discovery_uri = self.base_url + "/" + self.policy + "/discovery/v2.0/keys"
        self.other_discovery_uri = "https://login.microsoft.com/common/discovery/keys"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MSAuthAdapter, cls).__new__(cls)
        return cls.get_singleton_instance()

    @classmethod
    def get_singleton_instance(cls):
        if cls._instance is None:
            raise RuntimeError("Instance not initiated.")
        return cls._instance

    def decode_token(self, token: str) -> (bool, dict | PyJWTError):
        return True, {}
        try:
            key = self._get_key(token, self.discovery_uri)
            iss = self.issuer
            if key is None:
                key = self._get_key(token, self.other_discovery_uri)
                iss = self.other_issuer
            decoded_jwt: dict = jwt.decode(
                token,
                key,
                options={"verify_signature": True},
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=iss,
            )
            return True, decoded_jwt
        except PyJWTError as err:
            logger.warning("auth decode error: " + str(err))
            return False, err.args

    @cache
    def _get_key(self, token: str, discovery_uri: str) -> bytes | None:
        unverified_header = jwt.get_unverified_header(token)
        try:
            jwks = httpx.get(discovery_uri).json()["keys"]
        except json.JSONDecodeError:
            return None
        key_description = None
        for jwk in jwks:
            if jwk["kid"] == unverified_header["kid"]:
                key_description = jwk
                break
        if key_description is None:
            return None
        return self._convert_descriptor_to_pem_bytes(key_description)

    @staticmethod
    def _convert_str_to_bytes(value: str | bytes) -> bytes:
        if isinstance(value, str):
            value = value.encode("utf-8")
        return value

    def _base64_decode_to_int(self, value: str | bytes) -> int:
        decoded = base64.urlsafe_b64decode(self._convert_str_to_bytes(value) + b"==")
        return int.from_bytes(decoded, "big")

    def _convert_descriptor_to_pem_bytes(self, key_description: dict) -> bytes:
        return (
            RSAPublicNumbers(
                n=self._base64_decode_to_int(key_description["n"]),
                e=self._base64_decode_to_int(key_description["e"]),
            )
            .public_key(default_backend())
            .public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    def extract_claims(self, token: str):
        # not yet implemented
        pass
