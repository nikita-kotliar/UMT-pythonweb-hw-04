import asyncio
import argparse
import logging
from aiopath import AsyncPath
from aioshutil import copyfile


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Сортувати файли з вихідної папки"
    )
    parser.add_argument(
        "source",
        type=str,
        help="Шлях до вихідної папки.",
    )
    parser.add_argument(
        "output",
        type=str,
        help="Шлях до папки призначення.",
    )
    return parser.parse_args()

async def read_folder(source: AsyncPath, output: AsyncPath) -> None:
    files = []
    async for item in source.rglob("*"):
        if await item.is_file():
            files.append(item)

    async with asyncio.TaskGroup() as tg:
        for file in files:
            tg.create_task(copy_file(file, output))

async def copy_file(file: AsyncPath, output: AsyncPath) -> None:
    try:
        suffixes = file.suffixes
        
        full_suffix = suffixes[-1].lower() if suffixes else ""
        
        special_prefixes = {".tar", ".min", ".config", ".test"}

        if len(suffixes) >= 2:
            pre_suffix = suffixes[-2].lower()
            if pre_suffix in special_prefixes:
                full_suffix = (pre_suffix + suffixes[-1]).lower()

        folder_name = full_suffix.lstrip(".") if full_suffix else "no_extension"

        dest_dir = output / folder_name
        await dest_dir.mkdir(parents=True, exist_ok=True)

        if full_suffix:
            base_name = file.name[:-len(full_suffix)]
        else:
            base_name = file.name
        
        dest_file = dest_dir / file.name

        counter = 1
        while await dest_file.exists():
            dest_file = dest_dir / f"{base_name}_{counter}{full_suffix}"
            counter += 1

        await copyfile(file, dest_file)
        logger.info("Copied: %s → %s", file, dest_file)

    except Exception as error:
        logger.error("Failed to copy %s: %s", file, error)

    except Exception as error:
        logger.error("Failed to copy %s: %s", file, error)



async def main() -> None:
    args = parse_args()

    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    if not await source.exists() or not await source.is_dir():
        logger.error("Source folder '%s' does not exist or is not a directory.", source)
        return

    await output.mkdir(parents=True, exist_ok=True)

    await read_folder(source, output)
    logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
