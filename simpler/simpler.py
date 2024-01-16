####################################################################################################

import argparse
import logging
from pathlib import Path
from pprint import pprint

from colorama import Fore, Back, Style
import colorama
import fitz

####################################################################################################

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

colorama.init()

####################################################################################################

def on_pdf(path: Path)  -> None:
    # logging.info(f"{path}")
    print()
    print(Fore.BLUE + '_'*100)
    print(Fore.RED + f"{path.parent}")
    print(Fore.RED + f"  {path.name}")
    doc = fitz.open(str(path))
    for key in (
        'title',
        'keywords',
        # 'author',
        # 'modDate',
        # 'subject',
    ):
        _ = doc.metadata[key]
        print(Fore.BLUE + f"  {key}: {_}")
    # toc = doc.get_toc()
    # print(toc)
    page = doc.load_page(0)
    # text = page.get_text('text')
    # print(text)
    data = page.get_text('dict')
    # pprint(data)
    size_map = {}
    for block in data['blocks']:
        if 'lines' in block:
            for line in block['lines']:
                for span in line['spans']:
                    size = int(span['size'] * 100)
                    text = span['text']
                    # print(f"{size} {text}")
                    if text:
                        spans = size_map.setdefault(size, [])
                        spans.append(text)
    sizes = sorted(size_map.keys(), reverse=True)
    for size in sizes[:5]:
        for _ in size_map[size]:
            print(size, _)

####################################################################################################

def scan_directory(top_path: Path) -> None:
    for root, dirs, files in top_path.walk(
        top_down=True,
        on_error=None,
        follow_symlinks=False,
    ):
        root = Path(root)
        for filename in files:
            path = root.joinpath(filename)
            if path.suffix.lower() == '.pdf':
                on_pdf(path)

####################################################################################################

def main() -> None:
    parser = argparse.ArgumentParser(
        prog='',
        description='',
        epilog='',
        )

    parser.add_argument('path')
    args = parser.parse_args()
    logging.info("Start...")
    path = Path(args.path).resolve()
    if path.is_dir():
        scan_directory(path)
    logging.info("Done")

####################################################################################################

main()
