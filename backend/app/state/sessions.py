"""
In-memory conversation history, keyed by session_id.
Lost on server restart — will be replaced by Postgres persistence
in a later phase. Nothing outside this module should touch the
underlying dict directly.
"""

_session_histories: dict[str, list[dict]] = {}


def get_history(session_id: str) -> list[dict]:
    return _session_histories.setdefault(session_id, [])


def append_message(session_id: str, role: str, content: str) -> None:
    get_history(session_id).append({"role": role, "content": content})


def clear_session(session_id: str) -> None:
    _session_histories.pop(session_id, None)

def append_raw(session_id:str, raw:dict):
    get_history(session_id).append(raw)
