"""Small HTTP client used by the Streamlit frontend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass(slots=True)
class APIClientError(Exception):
    """A user-displayable backend communication error."""

    kind: str
    message: str
    status_code: int | None = None

    def __str__(self) -> str:
        return self.message


class NeuralForgeClient:
    """Typed boundary between Streamlit and the FastAPI service."""

    def __init__(self, base_url: str, timeout: int = 120) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def health(self, timeout: int = 4) -> dict[str, Any]:
        try:
            response = self._session.get(f"{self.base_url}/health", timeout=timeout)
            response.raise_for_status()
            payload = response.json()
            return payload if isinstance(payload, dict) else {}
        except (requests.ConnectionError, requests.Timeout) as exc:
            raise APIClientError(
                "unreachable",
                "The FastAPI backend is not reachable.",
            ) from exc
        except (requests.HTTPError, requests.JSONDecodeError) as exc:
            raise APIClientError(
                "backend",
                "The backend health check returned an invalid response.",
            ) from exc
        except requests.RequestException as exc:
            raise APIClientError(
                "unreachable",
                "The backend health check could not be completed.",
            ) from exc

    def analyze(self, endpoint: str, payload: dict[str, Any]) -> str:
        try:
            response = self._session.post(
                f"{self.base_url}{endpoint}",
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.ConnectionError as exc:
            raise APIClientError(
                "unreachable",
                "Cannot reach the backend. Start FastAPI and verify BACKEND_URL.",
            ) from exc
        except requests.Timeout as exc:
            raise APIClientError(
                "timeout",
                "The request timed out. Try a smaller input or retry in a moment.",
            ) from exc
        except requests.HTTPError as exc:
            raise self._from_http_error(exc.response) from exc
        except requests.JSONDecodeError as exc:
            raise APIClientError(
                "backend",
                "The backend returned a response that could not be read.",
            ) from exc
        except requests.RequestException as exc:
            raise APIClientError(
                "backend",
                "The backend request failed before a response was received.",
            ) from exc

        result = data.get("response") if isinstance(data, dict) else None
        if not isinstance(result, str) or not result.strip():
            raise APIClientError("backend", "The backend returned an empty AI response.")
        return result.strip()

    def upload(self, filename: str, content: bytes, task: str) -> str:
        try:
            response = self._session.post(
                f"{self.base_url}/upload-snippet",
                files={"file": (filename, content, "text/plain")},
                params={"task": task},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.ConnectionError as exc:
            raise APIClientError(
                "unreachable",
                "Cannot reach the backend. Start FastAPI and verify BACKEND_URL.",
            ) from exc
        except requests.Timeout as exc:
            raise APIClientError(
                "timeout",
                "The upload timed out. Try a smaller file or retry in a moment.",
            ) from exc
        except requests.HTTPError as exc:
            raise self._from_http_error(exc.response) from exc
        except requests.JSONDecodeError as exc:
            raise APIClientError(
                "backend",
                "The backend returned a response that could not be read.",
            ) from exc
        except requests.RequestException as exc:
            raise APIClientError(
                "backend",
                "The upload request failed before a response was received.",
            ) from exc

        result = data.get("response") if isinstance(data, dict) else None
        if not isinstance(result, str) or not result.strip():
            raise APIClientError("backend", "The backend returned an empty AI response.")
        return result.strip()

    @staticmethod
    def _from_http_error(response: requests.Response) -> APIClientError:
        status_code = response.status_code
        detail: Any = None
        try:
            detail = response.json().get("detail")
        except (ValueError, AttributeError):
            pass

        if isinstance(detail, list):
            messages = [
                str(item.get("msg", "Invalid input"))
                for item in detail
                if isinstance(item, dict)
            ]
            detail = "; ".join(messages)

        message = str(detail or f"Backend request failed with status {status_code}.")
        normalized_detail = message.lower()
        if status_code == 503 and (
            "not configured" in normalized_detail
            or "api key" in normalized_detail
        ):
            kind = "configuration"
        elif status_code in {502, 503} and "gemini" in normalized_detail:
            kind = "provider"
        else:
            kind = "backend"
        return APIClientError(kind, message, status_code)
