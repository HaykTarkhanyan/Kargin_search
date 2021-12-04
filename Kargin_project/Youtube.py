"""
    Written by asd on 04.12.21
"""

import logging

from googleapiclient.discovery import build

import pandas as pd
from datetime import timedelta
import re


class Youtube:
    """
    Class implements functions needed for scraping given youtube playlist and 
    returns `view_count, like_count, `
    """
    def __init__(self, api_key, playlist_id='PLC4FFB3F0AFB8146C'):
        """
        Args:
            api_key (str): Youtube API key
            playlist_id (str): playlist id to get data for, defaults to` PLC4FFB3F0AFB8146C
        """
        self.api_key = api_key
        self.playlist_id = playlist_id
        self.save_df_filepath = "../sample.csv"

        self.youtube = None
        self.vid_response = None
        self.videos = None
        self.results_df = None

    def connect(self):
        """
            Function connects to youtube server, uses  `self.api_key`
        """
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key, cache_discovery=False)
            return self.youtube

        except Exception as e:
            error_message = f"Error connection to youtube server: {e}"
            logging.critical(error_message)
            raise ValueError(error_message)
    

    def fetch_data_for_playlist(self, playlist_id=None):
        """
            Fetched reposnes for given playlist
        """
        
        if playlist_id is None:
            playlist_id = self.playlist_id

        nextPageToken = None
        while True:
            try:
                pl_request = self.youtube.playlistItems().list(
                                                        part='contentDetails',
                                                        playlistId=self.playlist_id,
                                                        maxResults=2_000,
                                                        pageToken=nextPageToken)

                pl_response = pl_request.execute()

                vid_ids = []
                for item in pl_response['items']:
                    vid_ids.append(item['contentDetails']['videoId'])

                vid_request = self.youtube.videos().list(
                    part=["statistics", "contentDetails"],
                    id=','.join(vid_ids)
                )

                vid_response = vid_request.execute()

            except Exception as e:
                error_message = f"Error gettig responses for playlist id {self.playlist_id}: {e}"
                logging.critical(error_message)
                raise ValueError(error_message)

# //////////////////////////////////////////////////////////////////////////////////////////////////
        
            # converting to list of dicts
            try:
                videos = []
                # regex for extracting video duration
                hours_pattern = re.compile(r'(\d+)H')
                minutes_pattern = re.compile(r'(\d+)M')
                seconds_pattern = re.compile(r'(\d+)S')

                for item in vid_response['items']:
                    duration = item['contentDetails']['duration']

                    hours = hours_pattern.search(duration)
                    minutes = minutes_pattern.search(duration)
                    seconds = seconds_pattern.search(duration)

                    hours = int(hours.group(1)) if hours else 0
                    minutes = int(minutes.group(1)) if minutes else 0
                    seconds = int(seconds.group(1)) if seconds else 0

                    video_seconds = timedelta(hours=hours,
                                              minutes=minutes,
                                              seconds=seconds).total_seconds()


                    vid_views = item['statistics']['viewCount']
                    likes = item['statistics']['likeCount']
                    dislikes = item['statistics']['dislikeCount']
                    comments = item['statistics']['commentCount']
                    duration = video_seconds

                    vid_id = item['id']
                    yt_link = f'https://youtu.be/{vid_id}'

                    videos.append(
                        {
                            'url': yt_link,
                            'views': int(vid_views),
                            'likes': int(likes),
                            'dislikes': int(dislikes),
                            'comments': int(comments),
                            'duration': duration
                        }
                    )

                nextPageToken = pl_response.get('nextPageToken')

                if not nextPageToken:
                    break

                self.videos = videos
                self.videos.sort(key=lambda vid: vid['views'], reverse=True)
                return self.videos
        
            except Exception as e:
                error_message = f'Error converting responses to list of dictionaries, {e}'
                logging.critical(error_message)
                raise ValueError(error_message) 



    # def extract_data_from_response(self):
    #     """
    #     Converts responses for videos to list of dictionaries with keys

    #                 'url': yt_link,
    #                 'views': int(vid_views),
    #                 'likes': int(likes),
    #                 'dislikes': int(dislikes),
    #                 'comments': int(comments),
    #                 'duration': duration
    #     """

        
    

    def convert_to_df_and_save(self, save_df_filepath=None):
        try:
            if save_df_filepath is None:
                save_df_filepath = self.save_df_filepath        


            self.df = pd.DataFrame(self.videos)
            self.df.to_csv(save_df_filepath)
            return self.df
        except Exception as e:
            error_message = f"Error converting {self.videos} to pd.DataFrame, or \
                              problem while saving to {save_df_filepath}: {e}"
            logging.critical(error_message) 
            raise ValueError(error_message) 
    

    def do_all(self):
        logging.debug('Trying to connect to Youtube API')
        self.connect()

        logging.debug('Trying to get responses for playlist and convert to list of dicts')
        self.fetch_data_for_playlist()

        # logging.debug('Trying to extract data from reponses')
        # self.extract_data_from_response()

        logging.debug("Tring to convert list of dicts to df and save it")
        self.convert_to_df_and_save()



Y = Youtube(api_key='AIzaSyCnmYbeQyboORylrdE3ljoOP9pJE9lOedg')
Y.do_all()   









