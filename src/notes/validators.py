import aiohttp
from fastapi import HTTPException
from fastapi import status

YANDEX_SPELLER_API_URL = (
    "https://speller.yandex.net/services/spellservice.json/checkText"
)


async def check_spelling(text: str) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            YANDEX_SPELLER_API_URL, data={"text": text}
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка при взаимодействии с API Яндекс.Спеллера",
                )
            errors = await response.json()
            return errors
