import asyncio

import logging
from pathlib import Path

import coloredlogs
import sys
import rich_click as click

from rich.console import Console
from rich.prompt import Prompt

from PIL.Image import Image

try:
    from . import scraper
except ImportError as ex:
    import scraper

# from rich.table import Table

logger = logging.getLogger(__name__)

logger_format = '%(asctime)s [%(name)s] %(module)s::%(funcName)s %(levelname)s - %(message)s'
coloredlogs.install(level='CRITICAL', fmt=logger_format)
coloredlogs.install(level='DEBUG', fmt=logger_format, logger=logger, stream=sys.stdout, isatty=True)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@click.group(invoke_without_command=True, context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('url', required=False, )
@click.argument('out_path', required=False, )
# @click.option('--workers', '-w', required=False, help='number of async scrapers', default=cr.DEFAULT_WORKERS_COUNT,
#               type=int)
def get_images(url, out_path):
    console = Console()
    while not url:
        url = Prompt(prompt='URL', console=console)()

    with console.status("Getting image...", spinner="monkey"):
        co = scraper.get_images(url)
        image: Image = loop.run_until_complete(co)

    if not out_path:
        default = Path().cwd() / 'saved_images'
        out_path = Prompt(prompt='Out Path', console=console)(default=str(default))
        if Path(out_path).resolve() == default.resolve():
            Path(out_path).mkdir(exist_ok=True)

    out_path = Path(out_path)
    if out_path.is_dir():
        file_path = out_path / 'cibus.png'
    else:
        file_path = out_path

    image.save(str(file_path))


get_images()
