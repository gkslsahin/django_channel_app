from io import StringIO

from django.test import TestCase
from .models import Channel, SubChannel, Content
from django.urls import reverse
from django.core.management import call_command
import unittest
import pathlib as pl
from csv import reader, DictReader


# Create your tests here.

class ChannelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tvshow = tvshow = Channel.objects.create(title="tvshows", image="tvshows_icon")
        cls.games = Channel.objects.create(title="Games", image="games_icon")
        cls.press_magazine = Channel.objects.create(title="Press&Mahazine", image="press_magazine_icon")

        cls.vikins = SubChannel.objects.create(title="vikins", image="viking.image.path",
                                               info_sub_channel="tv series about vikins", channel=cls.tvshow)
        cls.puzzle = SubChannel.objects.create(title="puzzle", image="puzzle.image.path",
                                               info_sub_channel="puzzle games",
                                               channel=cls.games)

        cls.viking_1_1 = Content.objects.create(sub_channel=cls.vikins, name="season 1 first episode",
                                                image="image.vikins.e1",
                                                language="tr,sp,en", content_info="this episiode about lorem ipsum1",
                                                rate=7,
                                                file="vikins1e1.mp4")
        cls.viking_1_2 = Content.objects.create(sub_channel=cls.vikins, name="season 1 second episode",
                                                image="image.vikins.e2",
                                                language="tr,sp,en", content_info="this episiode about lorem ipsum2",
                                                rate=4,
                                                file="vikins1e1.mp4")

        cls.lumen = Content.objects.create(sub_channel=cls.puzzle, name="lumen", image="image.games.lumen",
                                           language="en",
                                           content_info="enjoyable puzzle game", rate=6, file="lumen.apk")
        cls.candy_crush = Content.objects.create(sub_channel=cls.puzzle, name="candy_crush",
                                                 image="image.games.candy_crush",
                                                 language="en", content_info="most popular puzzle game", rate=10,
                                                 file="cany_crush.apk")

        cls.forbes = Content.objects.create(name="forbes_november", image="magazine.image.forbes",
                                            content_info="forbes magazine", channel=cls.press_magazine,
                                            file="forbes.pdf", rate=7,
                                            language="en")
        cls.time = Content.objects.create(name="time_november", image="magazine.image.time",
                                          content_info="time magazine",
                                          channel=cls.press_magazine, file="time.pdf", rate=4, language="en")
        cls.mens_health = Content.objects.create(name="mens_health", image="mens_health.image.path",
                                                 content_info="mens_health magazine", channel=cls.press_magazine,
                                                 file="mens_health.pdf", rate=9, language="en")

    def test_channel_model(self):
        self.assertEqual(self.tvshow.title, "tvshows")
        self.assertEqual(self.tvshow.image, "tvshows_icon")
        self.assertEqual(self.games.title, "Games")
        self.assertEqual(self.games.image, "games_icon")
        self.assertEqual(self.press_magazine.title, "Press&Mahazine")
        self.assertEqual(self.press_magazine.image, "press_magazine_icon")

    def test_sub_channel_model(self):
        self.assertEqual(self.vikins.title, "vikins")
        self.assertEqual(self.vikins.image, "viking.image.path")
        self.assertEqual(self.vikins.info_sub_channel, "tv series about vikins")
        self.assertEqual(self.vikins.channel, self.tvshow)

    def test_content_model(self):
        self.assertEqual(self.forbes.name, "forbes_november")
        self.assertEqual(self.forbes.image, "magazine.image.forbes")
        self.assertEqual(self.forbes.content_info, "forbes magazine")
        self.assertEqual(self.forbes.channel, self.press_magazine)
        self.assertEqual(self.forbes.file, "forbes.pdf")
        self.assertEqual(self.forbes.rate, 7)
        self.assertEqual(self.forbes.language, "en")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/api/channels/")
        self.assertEqual(response.status_code, 200)

    def test_get_apiView(self):
        response = self.client.get(reverse("channel"))
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get("/api/")
        self.assertEqual(no_response.status_code, 404)


class TestCaseBase(unittest.TestCase):
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            print(pl.Path(path).resolve())
            raise AssertionError("File does not exist: %s" % str(path))


class TestCSV(TestCaseBase):
    def test_check_csv_exists(self):
        path = pl.Path("channels_rate.csv")
        self.assertIsFile(path)
    def test_check_csv_data(self):
        # open file in read mode
        with open('channels_rate.csv', 'r',encoding='UTF-8') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = DictReader(read_obj)
            print(csv_reader)
            list_csv = list(csv_reader)
            self.assertEqual(list_csv[0]["channel"],"Games")
            self.assertEqual(list_csv[0]["average rating"],"8")

            self.assertEqual(list_csv[1]["channel"],"tvshows")
            self.assertEqual(list_csv[1]["average rating"],"7.75")

            self.assertEqual(list_csv[2]["channel"],"Press&Mahazine")
            self.assertEqual(list_csv[2]["average rating"],"6.666666666666667")