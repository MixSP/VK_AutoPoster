import datetime
from time import sleep
import os
import sys

import vk_api

from post import make_posts
from config import *


def make_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def two_factor():
    code = input('Enter 2FA code: ')
    remember_device = True
    return code, remember_device


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD,
                              auth_handler=two_factor,
                              app_id=APP_ID,
                              scope=PERMISSIONS,
                              config_filename='vk_config.v2.json')
    vk_session.auth()

    posts_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'posts')
    print('Posts: ')
    posts = make_posts(posts_path)
    print('=' * 40)

    for post in posts:
        td = ( post.time - datetime.datetime.now() ).total_seconds()
        if td < 0:
            print(post.time, '- wrong post time')
            print('-' * 40)
            continue

        else:
            while True:
                td = ( post.time - datetime.datetime.now() ).total_seconds()
                if td < 60:
                    try:
                        for GROUP_ID in GROUP_IDS:
                            print('[{}] Uploading files as attachments...'.format(make_time()))
                            post.upload_content(vk_session, USER_ID, GROUP_ID)

                            print('[{}] Posting to {}...'.format(make_time(), GROUP_ID))
                            post.post(vk_session, GROUP_ID)

                            print('[{}] Success!'.format(make_time()))
                            sleep(0.34)

                    except Exception as err:
                        print('[{}] {} - Error {}'.format(make_time(), post.time, err))

                    break

                else:
                    print('[{}] sleep {} min'.format(make_time(), round((td - 40) / 60, 1)))
                    sleep(td - 40)

        print('-' * 40)


if __name__ == '__main__':
    main()
