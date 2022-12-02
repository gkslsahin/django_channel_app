from django.core.management.base import BaseCommand
from django.utils import timezone
from channel.models import Channel
import statistics
import csv


class Command(BaseCommand):
    help = 'calculate channel rate'

    def create_csv(self,result_array):
        header = ['channel', 'average rating']
        with open('channels_rate.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            for data in result_array:
                writer.writerow(data)

    def calculate_rating(self):
        channels = Channel.objects.all()
        channel_rating = {}
        for channel in channels:
            channel_rating[str(channel)] = 0
            childs = channel.get_all_children()
            channel_rate_array = []
            for child in childs:
                if child.__class__.__name__ == "Content" and not child.sub_channel:
                    channel_rate_array.append(child.rate)
                elif child.__class__.__name__ == "SubChannel":
                    # calculate sub item rating
                    sub_item_rate_list = []
                    for sub_item in child.get_all_children():
                        if sub_item.__class__.__name__ == "Content":
                            sub_item_rate_list.append(sub_item.rate)
                    if len(sub_item_rate_list) > 0:
                        channel_rate_array.append(statistics.mean(sub_item_rate_list))
            channel_rating[str(channel)] = statistics.mean(channel_rate_array)
        result_list = sorted(channel_rating.items(), key=lambda item: item[1])
        return result_list[::-1]

    def handle(self, *args, **kwargs):

        self.create_csv(self.calculate_rating())

