"""CloudWatchログ書き込み用コード

| CloudWatch Logsへログを書き込む。
| 書き込む内容は任意のファイルに記載された内容を行単位で書き込む。

"""

import boto3
import sys
from enum import Enum
import configparser
import time


class Setting(Enum):
    """setting.ini 項目定義クラス

    setting.iniの項目を定義したクラス

    """
    LOG_GROUP_NAME = 'log_group_name'
    LOG_STREAM_NAME = 'log_stream_name'
    SOURCE_FILE = 'source_file'


# python実行時の引数読み込み
args = sys.argv
section = args[1]

# setting.iniの設定を読み込む
config = configparser.ConfigParser()
config.read('setting.ini')

# 書き込み対象のログを読み込み
f = open(config.get(section, Setting.SOURCE_FILE.value), 'r', encoding='UTF-8')
data_arr = f.read().split('\n')

# sequenceTokenを取得
f2 = open('sequenceToken.txt', 'r', encoding='UTF-8')
sequence_token = f2.read()

# CloudWatch Logsへログの書き込み
cw_client = boto3.client('logs')

for row in data_arr:
    response = cw_client.put_log_events(
        logGroupName=config.get(section, Setting.LOG_GROUP_NAME.value),
        logStreamName=config.get(section, Setting.LOG_STREAM_NAME.value),
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': row
            }
        ],
        sequenceToken=sequence_token
    )
    sequence_token = response.get('nextSequenceToken', '')

# sequenceTokenの書き込み
f3 = open('sequenceToken.txt', 'w', encoding='UTF-8')
f3.write(sequence_token)
f3.close()
