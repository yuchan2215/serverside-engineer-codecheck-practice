import csv
import sys
from argparse import ArgumentParser, Namespace

from player import Player


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
players: dict = {}  # プレイヤー一覧を入れていく辞書


def getPlayer(playerId: str) -> Player:
    """
    辞書からプレイヤーを探します。無ければ新しく作ります。

    :param playerId: プレイヤーID
    :return: プレイヤー
    """
    if playerId in players:
        # もし含まれるのであればその値を返す
        return players.get(playerId)
    else:
        # もし含まれないなら新しく生成して返す。

        player = Player()  # 新規プレイヤー
        players[playerId] = player  # 辞書に追加
        return player


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

    # 最初の行で無ければ行の読み込み機能を作っていく。
    # 日付は扱わないのでプログラム内で取り扱わない。
    name = str(row[1])
    score = int(row[2])

    # プレイヤーを辞書から取得し、結果を追加する。
    getPlayer(name).addResult(score)


def readCsv():
    """
    CSVを読み込みます。
    """
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # 行の読み込みを行う。
            readRow(row=row)


if __name__ == "__main__":
    # コマンドライン引数の読み取り
    args = get_option()
    fileName = str(args.fileName)

    # CSVを読み込む（エラーがあれば出力する。）
    error = True
    try:
        readCsv()
    except FileNotFoundError:
        print(f'"{fileName}"というファイルは見つかりませんでした。')
    except IsADirectoryError:
        print('ディレクトリが指定されています')
    except PermissionError as e:
        print('権限がありません\n', e)
    except ValueError as e:
        print('CSVの値に想定外のものがありました\n', e)
    except Exception as e:
        print('CSVの読み込みに失敗しました\n', e)
    else:
        error = False

    if error:
        # エラーがあったのであればプログラムを終了する。
        sys.exit(1)
