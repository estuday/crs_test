from nova.sdk.llm.spark.client import Spark
from dotenv import load_dotenv

load_dotenv()
from nova.data.logos import Logos

llm = Spark()
import asyncio


async def main():
    rsp = await llm.acall([Logos(role=Logos.Role.USER, content="你好")])
    print(rsp)


asyncio.run(main())
