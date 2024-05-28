from typing import AsyncGenerator, List, Dict
import colorama
import aiohttp
import secrets
import asyncio
import ujson
import random
import re

########################################################################
# Credits to .puzzy.                                                   #
# https://shard-ai.xyz                                                 #
# discord.gg/ligma                                                     #
# Dear skids, smd :)                                                   #
########################################################################

async def image(prompt: str, url: str, proxy: str = None) -> str:
    print(prompt, proxy)
    """
    Generate an image using the Hugging Face API.

    Args:
        prompt (str): The prompt to generate the image.
        url (str): The Hugging Face space URL.
        proxy (str): The proxy to use (optional).

    Returns:
        str: The URL of the generated image, or False if an error occurs.
    """
    try:
        session_hash = secrets.token_hex(11)
        join_url = f"{url}/queue/join?"
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': f'{url}',
            'priority': 'u=1, i',
            'referer': f'{url}/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
        get_url = f"{url}/queue/data?session_hash={session_hash}"
        data = {
            "data": [
                f"{prompt}",
                f"ugly, bad",
                '(LoRA)',
                True,
                20,
                1,
                random.randint(1, 10000),
                1024,
                1024,
                6,
                True
            ],
            "event_data": None,
            "fn_index": 3,
            "trigger_id": 6,
            "session_hash": session_hash
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url=join_url, headers=headers, json=data, proxy=proxy) as response:
                if response.status != 200:
                    print(response.status)
                    return False

            async with session.get(url=get_url, headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content.iter_any():
                    data = chunk.decode('utf-8', 'ignore')
                    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+|ftp://[^\s<>"]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s<>"]*)?', data)
                    for obj in urls:
                        if "http" in obj:
                            return obj  # URL found
    except Exception as e:
        print(f"Failed to generate image, why? {str(e)}")
        return False

async def text(history: List[Dict[str, str]], url: str) -> AsyncGenerator:
    """
    Generate text using the Hugging Face API.

    Args:
        history (List[Dict[str, str]]): The chat history.
        url (str): The Hugging Face space URL.

    Returns:
        AsyncGenerator: An async generator yielding the generated text.
    """
    # TODO: Implement text generation functionality
    pass

async def main():
    """
    Main script function.
    """
    running = True
    while running:
        model_type: str = input(f"{colorama.Fore.LIGHTCYAN_EX}Welcome to the Hugging Face reverse! Type the desired type of model you'll like to use. [image, text]: ")
        url: str = input("What is the Hugging Face space URL you'll like to use (don't include trailing slash): ")
        proxy: str | None = input("Proxy (leave empty if you don't have one): ")

        if model_type.lower() == "image":
            while True:
                prompt = str(input("What would you like to make: "))
                print("Generating your image...")
                image_url = await image(prompt, url, proxy)
                if image_url:
                    print(f"Done! Here is the image URL: {image_url}")
                else:
                    print("Failed to generate the image.")

                generate_another = input("Would you like to generate another image? (y/n): ")
                if generate_another.lower() != 'y':
                    break

        elif model_type.lower() == "text":
            # TODO: Implement text generation functionality
            pass

        elif model_type.lower() in ["exit", "leave", "bye"]:
            print("Goodbye!")
            await asyncio.sleep(3)
            running = False

        else:
            print("Invalid command!")
            continue

if __name__ == "__main__":
    asyncio.run(main())