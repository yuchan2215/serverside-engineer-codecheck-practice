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


def dicSort() -> list:
    """
    プレイヤーの辞書を平均得点順でソートします。
    :return: ソートされたリストです。
    """
    global players

    return sorted(players.items(), key=lambda p: p[1].getAverage(), reverse=True)


def output(playersList: list):
    """
    結果を出力します
    :param playersList: プレイヤーのリスト
    """
    count = 0  # 順位重複関係なく増える値
    rank = 0  # 順位重複を考慮した値
    cacheScore = None  # 順位重複を考慮するためのキャッシュ

    print("rank,player_id,mean_score")
    for i in playersList:
        playerId: str = i[0]
        player: Player = i[1]

        avg = player.getAverage()
        count += 1

        # 点数変動があるなら
        if cacheScore != avg:
            if count > 10:
                # 生の順位が11を超えているなら抜ける
                break

            rank = count  # ランク更新する
            cacheScore = avg  # キャッシュを更新する

        print(f'{rank},{playerId},{avg}')


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

    sortedList = dicSort()  # ソートする
    output(sortedList)  # 出力する
