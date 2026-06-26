"""
initializer.py

アプリケーションの初期設定を行うクラス
"""

from enum import Enum, auto
from pathlib import Path


class InitializeMode(Enum):
    """初期化モード"""

    INTERACTIVE = auto()      # 対話形式
    NON_INTERACTIVE = auto()  # 非対話形式


class Initializer:
    """アプリケーションの初期設定を行うクラス"""

    def __init__(self, mode: InitializeMode = InitializeMode.INTERACTIVE) -> None:
        """
        コンストラクタ

        Args:
            mode: 初期化モード
        """
        self._mode = mode
        self._project_root = Path(__file__).resolve().parents[2]
        self._env_file = self._project_root / ".env"

    def run(self) -> None:
        """
        初期設定を実行する
        """

        if not self._env_file.exists():
            self._create_env()

    def _create_env(self) -> None:
        """
        .envファイルを生成する
        """

        if self._mode == InitializeMode.INTERACTIVE:
            print(".env が存在しません。初期設定を開始します。")

            api_key = input("Riot API Key : ").strip()
            game_name = input("Riot Game Name : ").strip()
            tag_line = input("Riot Tag Line : ").strip()

            self._env_file.write_text(
                "\n".join(
                    [
                        f"RIOT_API_KEY={api_key}",
                        f"RIOT_GAME_NAME={game_name}",
                        f"RIOT_TAG_LINE={tag_line}",
                    ]
                ),
                encoding="utf-8",
            )

            print(".env を作成しました。")

        else:
            raise FileNotFoundError(
                ".env が存在しません。NON_INTERACTIVEモードでは自動生成できません。"
            )