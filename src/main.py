from argparse import ArgumentParser, Namespace


def get_option() -> Namespace:
    """
    プログラムに渡された引数を取得します。
    :return: 引数から渡された値
    """
    _argParser = ArgumentParser()
    _argParser.add_argument('fileName', type=str, help="利用するCSVファイル名を指定します。")
    return _argParser.parse_args()


if __name__ == "__main__":
    # コマンドライン引数の読み取り
    args = get_option()
    fileName = str(args.fileName)
