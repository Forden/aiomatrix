import json
import pathlib
import unittest
from typing import Tuple, TypeVar

from aiomatrix import types

T = TypeVar('T')
cwd = pathlib.Path(__file__).parent


def read_file(path: pathlib.Path) -> Tuple[dict, str]:
    with open(path, encoding='utf8', mode='r') as f:
        result = json.load(f)
    return result, json.dumps(result, sort_keys=True)


class TestTextContent(unittest.TestCase):
    raw: dict
    content: types.events.modules.instant_messaging.AudioContent

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.json = read_file(cwd / 'data' / 'content' / 'text.json')
        cls.content = types.events.modules.instant_messaging.AudioContent(**cls.raw)

    def test_parse(self):
        parse_from_file(cwd / 'data' / 'content' / 'text.json', types.events.modules.instant_messaging.TextContent)

    def test_body(self):
        self.assertEqual(self.raw['body'], self.content.body)

    def test_export(self):
        self.assertEqual(
            self.json,
            self.content.json(by_alias=True, exclude_unset=True, exclude={'raw'}, **{'sort_keys': True})
        )


def parse_from_file(path: pathlib.Path, model: T) -> Tuple[dict, T]:
    raw, _ = read_file(path)
    return raw, model(**raw)


class TestAudioContent(unittest.TestCase):
    raw: dict
    content: types.events.modules.instant_messaging.AudioContent

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.json = read_file(cwd / 'data' / 'content' / 'audio.json')
        cls.content = types.events.modules.instant_messaging.AudioContent(**cls.raw)

    def test_parse(self):
        parse_from_file(cwd / 'data' / 'content' / 'audio.json', types.events.modules.instant_messaging.AudioContent)

    def test_body(self):
        self.assertEqual(self.raw['body'], self.content.body)

    def test_info(self):
        self.assertEqual('info' in self.raw, self.content.info is not None)
        self.assertEqual(
            self.raw['info']['duration'] if 'info' in self.raw else None,
            self.content.info.duration if 'info' in self.raw else None
        )
        self.assertEqual(
            json.dumps(self.raw['info'], sort_keys=True),
            self.content.info.json(by_alias=True, exclude_unset=True, exclude={'raw'}, **{'sort_keys': True})
        )

    def test_url(self):
        self.assertEqual('url' in self.raw, self.content.url is not None)
        self.assertEqual(self.raw['url'] if 'url' in self.raw else None, self.content.url)

    def test_export(self):
        self.assertEqual(
            self.json,
            self.content.json(by_alias=True, exclude_unset=True, exclude={'raw'}, **{'sort_keys': True})
        )


class TestImageContent(unittest.TestCase):
    raw: dict
    content: types.events.modules.instant_messaging.ImageContent

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw, cls.json = read_file(cwd / 'data' / 'content' / 'image.json')
        cls.content = types.events.modules.instant_messaging.ImageContent(**cls.raw)

    def test_parse(self):
        parse_from_file(cwd / 'data' / 'content' / 'image.json', types.events.modules.instant_messaging.ImageContent)

    def test_body(self):
        self.assertEqual(self.raw['body'], self.content.body)

    def test_info(self):
        self.assertEqual('info' in self.raw, self.content.info is not None)
        expected_thumnail_url = None
        if 'info' in self.raw:
            expected_thumnail_url = self.raw['info'].get('thumbnail_url', None)
        self.assertEqual(
            expected_thumnail_url,
            self.content.info.thumbnail_url if 'info' in self.raw else None
        )
        expected_thumbnail_info_h = None
        expected_thumbnail_info_w = None
        if 'info' in self.raw:
            if 'thumnail_info' in self.raw['info']:
                expected_thumbnail_info_h = self.raw['info']['thumbnail_info']['h']
                expected_thumbnail_info_w = self.raw['info']['thumbnail_info']['w']
        self.assertEqual(
            expected_thumbnail_info_h,
            self.content.info.thumbnail_info.h if 'info' in self.raw and 'thumbnail_info' in self.raw['info'] else None
        )
        self.assertEqual(
            expected_thumbnail_info_w,
            self.content.info.thumbnail_info.w if 'info' in self.raw and 'thumbnail_info' in self.raw['info'] else None
        )
        self.assertEqual(
            json.dumps(self.raw['info'], sort_keys=True),
            self.content.info.json(by_alias=True, exclude_unset=True, exclude={'raw'}, **{'sort_keys': True})
        )

    def test_url(self):
        self.assertEqual('url' in self.raw, self.content.url is not None)
        self.assertEqual(self.raw['url'] if 'url' in self.raw else None, self.content.url)

    def test_export(self):
        self.assertEqual(
            self.json,
            self.content.json(by_alias=True, exclude_unset=True, exclude={'raw'}, **{'sort_keys': True})
        )
