####################################################################################################
#
# progress => yield -> list
#
#
####################################################################################################

from pathlib import Path
from pprint import pprint
from typing import Self, Generator
import argparse
import logging
import os
import subprocess

from colorama import Fore
import colorama
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

import fitz

####################################################################################################

DRY_RUN = False

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

colorama.init()

style = Style.from_dict({
# User input (default text)
'': '#000000',
# Prompt
'prompt': '#ff0000',
# Output
# 'red': '#ff0000',
# 'green': '#00ff00',
# 'blue': '#0000ff',
})

####################################################################################################

def rprint(*args) -> None:
    print(*args, Fore.BLACK)

####################################################################################################

class PdfDocument:

    ##############################################

    def __init__(self: Self, path: Path) -> None:
        self._path = Path(path)
        self._doc = None
        # logging.info(f"{path}")

    ##############################################

    @property
    def parent(self: Self) -> Path:
        return self._path.parent

    @property
    def name(self: Self) -> str:
        return self._path.name

    ##############################################

    def print_name(self: Self) -> None:
        print()
        rprint(Fore.BLUE + '_'*100)
        rprint(f"{Fore.RED}{self.parent}")
        rprint(f"  {Fore.RED}{self.name}")

    ##############################################

    def rename_if_exists(self: Self, filename: str) -> str:
        _ = filename
        stem = Path(_).stem
        suffix = Path(_).suffix
        def to_abs(x: str) -> Path:
            return self.parent.joinpath(x)
        i = 0
        while to_abs(_).exists():
            i += 1
            _ = f'{stem}---{i}{suffix}'
        return _

    ##############################################

    def better_name(self: Self) -> str:
        _ = self.name
        for i in range(20):
            _ = _.replace(f'({i})', f'---{i}')
        for c in ("&()'"):
            _ =_ .replace(c, '')
        for args in (
            (',', '_'),
            (' ', '_'),
            ('_-_', '-'),
            ('___', '_'),
            ('__', '_'),
            ('_.', '.'),
            ('._', '_'),
            ('..', '.'),
        ):
            _ =_ .replace(*args)
        if _ and _ != self.name:
            return self.rename_if_exists(_)
            # return _
        else:
            return None

    ##############################################

    def fix_name(self: Self) -> None:
        new_filename = self.better_name()
        if new_filename is not None:
            self.print_name()
            rprint(f'{Fore.RED}rename {Fore.BLUE}{self.name}')
            rprint(f'  to {Fore.BLUE}{new_filename}')
            self.rename(new_filename)

    ##############################################

    def load_pdf(self: Self) -> None:
        if self._doc is not None:
            return
        try:
            self._doc = fitz.open(str(self._path))
            self._page = self._doc.load_page(0)
        except fitz.fitz.FileDataError:
            rprint(f"{Fore.RED} File Error")

    ##############################################

    def dump(self: Self) -> None:
        self.load_pdf()
        if self._doc is None:
            return
        for key in (
            'title',
            'keywords',
            # 'author',
            # 'modDate',
            # 'subject',
        ):
            _ = self._doc.metadata[key]
            print(Fore.BLUE + f"  {key}: {_}")
        # toc = doc.get_toc()
        # print(toc)
        # text = page.get_text('text')
        # print(text)
        data = self._page.get_text('dict')
        # pprint(data)
        size_map = {}
        for block in data['blocks']:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        size = int(span['size'] * 100)
                        text = span['text'].strip()
                        # print(f"{size} {text}")
                        if text:
                            spans = size_map.setdefault(size, [])
                            spans.append(text)
        sizes = sorted(size_map.keys(), reverse=True)
        for size in sizes[:5]:
            for _ in size_map[size]:
                print(size, _)

    ##############################################

    def search(self: Self, keyword: str) -> bool:
        self.load_pdf()
        if self._doc is None:
            return False
        areas = self._page.search_for(keyword)
        if areas:
            data = self._page.get_text('dict')
            for block in data['blocks']:
                if 'lines' in block:
                    for line in block['lines']:
                        for span in line['spans']:
                            text = span['text']
                            if keyword in text:
                                print(text)
                                return True
        return False

    ##############################################

    def usage(self: Self) -> None:
        for _ in (
                'exit using command <blue>quit</blue> or <blue>Ctrl+d</blue>',
        ):
            print_formatted_text(
                HTML(_),
            style=style,
            )

    ##############################################

    def cli(self: Self) -> None:
        completer = WordCompleter([
            'rename',
            'open',
        ])
        session = PromptSession(
            completer=completer,
        )
        self.usage()
        while True:
            try:
                message = [
                    ('class:prompt', '> '),
                ]
                query = session.prompt(
                    message,
                    style=style,
                )
            except KeyboardInterrupt:
                exit()
                # continue
            except EOFError:
                break
            else:
                if not query:
                    self.usage()
                    continue
                query = query.strip()
                command = None
                if ' ' in query:
                    try:
                        command, argument = query.split()
                    except ValueError:
                        pass
                else:
                    command = query
                match command:
                    case 'quit':
                        break
                    case 'open':
                        self.open()
                    case 'rename':
                        self.rename(argument)
                    case _:
                        self.usage()
                        continue

    ##############################################

    def open(self: Self) -> None:
        command = ('/usr/bin/xdg-open', str(self._path))
        subprocess.call(command)

    ##############################################

    def rename(self: Self, filename: str) -> None:
        new_path = self.parent.joinpath(filename)
        if not new_path.exists():
            if not DRY_RUN:
                #  path.rename(new_path)   # don't raise
                os.rename(self._path, new_path)
                rprint(f'renamed to {Fore.BLUE}{filename}')
        else:
            rprint(f"  {Fore.RED}error: file exists")

####################################################################################################

class DirectoryScanner:

    ##############################################

    def __init__(self: Self, top_path: str | Path) -> None:
        self._top_path = Path(top_path)

    ##############################################

    def scan(self: Self, **kwargs) -> Generator(str, None, None):
        file_counter = 0
        for root, dirs, files in self._top_path.walk(
            top_down=True,
            on_error=None,
            follow_symlinks=False,
        ):
            root = Path(root)
            for filename in files:
                _ = root.joinpath(filename)
                if self.on_file(_, kwargs):
                    file_counter += 1
                    yield _
        print()
        rprint(f"Found {Fore.RED}{file_counter}{Fore.BLACK} files")

    ##############################################

    def on_file(self: Self, path: Path, kwargs) -> None:
        if path.suffix.lower() == '.pdf':
            self.on_pdf(path, kwargs)
            return True
        return False

    ##############################################

    def on_pdf(self: Self, path: Path, kwargs: dict) -> None:
        try:
            _ = PdfDocument(path)
            # _.fix_name()
            # _.print_name()
            # _.dump()
            # _.cli()
            if 'search' in kwargs:
                if _.search(kwargs['search']):
                    _.print_name()
        except (UnicodeDecodeError, UnicodeEncodeError):
            rprint(f"{Fore.RED} Unicode error")

####################################################################################################

def main() -> None:
    parser = argparse.ArgumentParser(
        prog='',
        description='',
        epilog='',
    )

    parser.add_argument('path')
    parser.add_argument(
        '--dry-run',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '--search',
        default=None
    )
    args = parser.parse_args()
    # logging.info("Start...")
    if args.dry_run:
        global DRY_RUN
        DRY_RUN = True
        rprint(f"{Fore.RED}Set to dry run")
    path = Path(args.path).resolve()
    if path.is_dir():
        _ = DirectoryScanner(path)
        _.scan(
            search=args.search,
        )
    print()
    rprint(f"{Fore.RED}Done")
    # logging.info("Done")

####################################################################################################

main()
