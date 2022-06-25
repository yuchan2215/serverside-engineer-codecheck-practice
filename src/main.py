import csv
import itertools
import sys
from argparse import ArgumentParser, Namespace
from typing import Dict, List

# CSVに対応するタイトル。
PLAYER_ID_COLUMN = 'player_id'
SCORE_COLUMN = 'score'

# 出力するプレイヤー数
REPORT_PLAYERS = 10


class Player:
    """
    プレイヤー型。
    省メモリを実現するために、辞書と併用して利用することを想定してプレイヤーIDは保持していません。
    """
    _gameCount: int = 0  # プレイしたゲームの数
    _sumScore: int = 0  # 合計スコア

    def getAverage(self) -> int:
        """
        プレイヤーの平均スコアを計算します。
        :return: 四捨五入された平均スコアです。
        """
        if self._gameCount == 0:
            # 0除算対策
            return 0

        # 平均を返す
        return round(self._sumScore / self._gameCount)

    def addResult(self, score: int):
        """
        ゲームの結果を追加します。
        :param score: 加算するスコア
        """

        # ゲームのカウント値とスコアを変動させる。
        self._gameCount += 1
        self._sumScore += score


class RankingObject:
    """
    ランキングに使用するオブジェクト。
    同一スコアのプレイヤーをまとめるために使用します。
    """
    score: int
    playerIds: List[str]

    def __init__(self, score: int, playerIds: List[str]):
        self.score = score
        self.playerIds = playerIds


def get_option() -> Namespace:
    """
    プログラムに渡された引数を取得します。
    :return: 引数から渡された値
    """
    _argParser = ArgumentParser()
    _argParser.add_argument('fileName', type=str, help="利用するCSVファイル名を指定します。")
    return _argParser.parse_args()


def readCsv(fileName: str) -> Dict[str, Player]:
    """
    CSVからプレイヤーのデータを読み込みます。
    :param fileName: 読み込むCSVファイルのパス
    :return: 読み込み結果をPlayerオブジェクトに入れた辞書型ファイル。
    """
    records: Dict[str, Player] = {}

    with open(fileName, 'r') as f:
        reader = csv.DictReader(f, lineterminator="\n")
        for row in reader:
            # CSVの内容を読み込む
            player_id = row[PLAYER_ID_COLUMN]
            score = int(row[SCORE_COLUMN])
            # レコードがないなら作成する
            if player_id not in records:
                records[player_id] = Player()
            # レコードの内容を書き換える
            record = records[player_id]
            record.addResult(score)
    return records


def mean_by_player(records: Dict[str, Player]) -> Dict[str, int]:
    """
    プレイヤーの平均点を求めた辞書を作成します。
    算出方法はPlayerクラスに依存します。
    :param records: プレイヤー一覧のレコード
    :return: プレイヤーごとの平均点の辞書
    """
    means: Dict[str, int] = {}

    for playerId, record in records.items():
        means[playerId] = record.getAverage()

    return means


def make_ranking(means: Dict[str, int]) -> Dict[int, RankingObject]:
    """
    平均点によるランキングを作成します。
    同一点数のものは、同一順位として扱います。
    :param means: プレイヤーごとの平均点の辞書
    :return: 順位ごとのRankingObjectの辞書
    """
    # 点数降順でソートする。
    sorted_means = sorted(means.items(), reverse=True, key=lambda x: x[1])
    # 点数ごとにまとめる。
    grouped_means = itertools.groupby(sorted_means, lambda x: x[1])

    ranking_data: Dict[int, RankingObject] = {}
    rank = 1

    for score, player_id_and_score in grouped_means:
        # groupByしたアイテムの中から、player_idを引っ張り出してくる。
        player_ids = list(map(lambda x: x[0], list(player_id_and_score)))

        # 反映させる。
        ranking_data[rank] = RankingObject(score, player_ids)
        rank += len(player_ids)

    return ranking_data


def output(rankDict: Dict[int, RankingObject], report_players: int = REPORT_PLAYERS):
    """
    ランキングを出力します。
    同じ順位のプレイヤーが複数いる場合は、プレイヤー名昇順で出力します。
    :param rankDict: ランキング形式の辞書
    :param report_players: 発表するプレイヤー数
    """
    print("rank,player_id,mean_score")
    printed = 0
    for (rank, rankingObj) in rankDict.items():
        rank: int
        rankingObj: RankingObject

        # 出力した件数が出力する順位以上であれば抜ける。
        if report_players <= printed:
            break

        # プレイヤー名昇順で出力する。
        sorted_player_ids = sorted(rankingObj.playerIds)
        for player_id in sorted_player_ids:
            print(f"{rank},{player_id},{rankingObj.score}")

        # 印刷件数を変える。
        printed += len(sorted_player_ids)


def main():
    # コマンドライン引数の読み取り
    args = get_option()
    fileName = str(args.fileName)

    # CSVを読み込む（エラーがあれば出力する。）
    error = True
    records: Dict[str, Player] = {}
    try:
        records = readCsv(fileName)
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

    player_mean_scores = mean_by_player(records)
    ranking_dict = make_ranking(player_mean_scores)
    output(ranking_dict)


if __name__ == "__main__":
    main()
