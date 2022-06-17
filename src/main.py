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


def formatCheck(row: list) -> bool:
    """
    １行目が想定されているものかどうかチェックします。

    :param row: １行目のリスト。
    :return: rowが想定されているものと一致しているか
    """
    return row == ['create_timestamp', 'player_id', 'score']


readFirst: bool = False  # 最初の行を読み込んだか


def readRow(row: list):
    """
    １行ずつ読み込みます。
    :param row: 行のデータ
    """
    global readFirst

    if not readFirst:
        # もし最初の行であれば、フォーマットチェックを行う
        readFirst = True
        format_correct = formatCheck(row)

        if not format_correct:
            # 失敗したならエラーを出す。
            raise FormatError()

        else:
            # 成功したなら早期リターンをする。
            return

    # TODO ANY


def readCsv():
    with open(fileName) as f:
        reader = csv.reader(f)
        for row in reader:
            # 行の読み込みを行う。
            readRow(row=row)


if __name__ == "__main__":
    # コマンドライン引数の読み取り
    args = get_option()
    fileName = str(args.fileName)
