import asyncio
import os
from core.piyolog_parser.piyolog_parser_month import PiyoLogParserMonth
from logger_factory import LoggerFactory

logger = LoggerFactory.getLogger(__name__)

src_dir = "piyolog_data"


async def main():

    file_list = []
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            # フルパスで取得する場合：
            file_path = os.path.join(dirpath, filename)
            file_list.append(file_path)

    parser = PiyoLogParserMonth()

    for file in file_list:
        logger.info(f"file: {file}")

        with open(file, "r") as f:
            content = f.read()
            data = parser.parse_str(content)
            logger.debug(data)


if __name__ == "__main__":
    asyncio.run(main())
