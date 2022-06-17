class Player:
    # 結果を全て配列にするとメモリが圧迫されるため、int型の2つだけ用意して管理する。
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
