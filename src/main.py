import csv
from argparse import ArgumentParser, Namespace


class FormatError(Exception):
    """フォーマットが正しく無い時に呼び出されます。"""
    pass


def get_option() -> Namespace:
    """
    プログラムに渡された引数を取得します。
    :return: 引数から渡された値
    """
    _argParser = ArgumentParser()
    _argParser.add_argument('fileName', type=str, help="利用するCSVファイル名を指定します。")
    return _argParser.parse_args()


def readCsv():
    with open(fileName) as f:
        reader = csv.reader(f)
        for row in reader:
            pass  # TODO any


if __name__ == "__main__":
    # コマンドライン引数の読み取り
    args = get_option()
    fileName = str(args.fileName)
