import pytest
from fastapi import HTTPException
from app.services.llm_provider import fallback_chain


@pytest.mark.asyncio
async def test_fallback_chain_returns_first_success():
    async def first():
        return "ok1"

    async def second():
        return "ok2"

    result, provider = await fallback_chain([("first", first), ("second", second)])

    assert result == "ok1"
    assert provider == "first"


@pytest.mark.asyncio
async def test_fallback_chain_falls_back_on_exception():
    async def fail():
        raise Exception("fail")

    async def second():
        return "ok2"

    result, provider = await fallback_chain([("fail", fail), ("second", second)])

    assert result == "ok2"
    assert provider == "second"


@pytest.mark.asyncio
async def test_fallback_chain_all_fail():
    async def fail1():
        raise Exception("fail1")

    async def fail2():
        raise Exception("fail2")

    with pytest.raises(HTTPException) as exc_info:
        await fallback_chain([("fail1", fail1), ("fail2", fail2)])

    assert exc_info.value.status_code == 503
