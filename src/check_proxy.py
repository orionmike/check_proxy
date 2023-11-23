import asyncio
import json
from pathlib import Path
import aiohttp

from config import ABS_PATH, CHECK_PROXY_URL


def get_proxy_list(file_name: str) -> list:
    proxy_list = []
    with open(file_name, 'r') as file:
        for line in file:
            proxy_list.append(f'http://{line.strip()}')

    return proxy_list


async def check_responce(response, proxy):
    if response:
        result = await response.text()

        if result:
            try:
                json_result = json.loads(result)
            except:
                json_result = None

            if json_result:
                if json_result.get('connect'):
                    print(f"{proxy} -> {json_result['connect']}")


async def check_proxy(url, proxy) -> bool:

    async with aiohttp.ClientSession() as session:

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
        }

        try:
            response = await session.get(url, proxy=proxy, headers=headers, timeout=3)
        except:
            response = None

        await check_responce(response, proxy)


async def main() -> None:

    file = Path(f'{ABS_PATH}/proxy_list.txt')
    proxy_list = get_proxy_list(file)
    # print(proxy_list)

    task_list = []

    for proxy in proxy_list:
        task = asyncio.create_task(check_proxy(CHECK_PROXY_URL, proxy))
        task_list.append(task)

    await asyncio.gather(*task_list)


if __name__ == "__main__":
    asyncio.run(main())
