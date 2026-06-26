"""
config_manager.py

アプリケーション設定を管理するモジュール。

設定ファイル(settings.yaml)および環境変数(.env)を読み込み、
アプリケーション全体へ設定値を提供する。
"""

from pathlib import Path
from typing import Any
from os import getenv

import yaml
from dotenv import load_dotenv


class ConfigManager:
    """
    アプリケーション設定管理クラス。

    本クラスは設定ファイルおよび環境変数を一度だけ読み込み、
    各モジュールへ設定値を提供する。

    インスタンス生成は禁止されている。
    """
    #
    # Project
    #
    _PROJECT_ROOT = Path(__file__).resolve().parents[2]

    #
    # File Path
    #
    _SETTINGS_PATH = (
        _PROJECT_ROOT
        / "config"
        / "settings.yaml"
    )

    _ENV_PATH = (
        _PROJECT_ROOT
        / ".env"
    )

    #
    # State
    #
    _initialized = False
    _settings: dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        """
        インスタンス生成を禁止する。

        Raises:
            TypeError:
                インスタンス生成が要求された場合。
        """
        raise TypeError(
            "ConfigManager cannot be instantiated. "
            "Use ConfigManager.initialize()."
        )

    #
    # Lifecycle
    #
    @classmethod
    def initialize(cls) -> None:
        """
        ConfigManagerを初期化する。

        settings.yamlおよび.envを読み込む。
        """

        if cls._initialized:
            return

        #
        # settings.yaml
        #
        if not cls._SETTINGS_PATH.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {cls._SETTINGS_PATH}"
            )

        with cls._SETTINGS_PATH.open(
            mode="r",
            encoding="utf-8"
        ) as file:

            loaded = yaml.safe_load(file)

            if loaded is None:
                loaded = {}

            if not isinstance(loaded, dict):
                raise TypeError(
                    "settings.yaml must contain a dictionary."
                )

            cls._settings = loaded

        #
        # .env
        #
        if cls._ENV_PATH.exists():
            load_dotenv(cls._ENV_PATH)

        cls._initialized = True

    @classmethod
    def reload(cls) -> None:
        """
        設定ファイルおよび環境変数を再読み込みする。

        本メソッドは現在保持している設定を破棄し、
        settings.yaml および .env を再度読み込む。
        """

        cls._initialized = False
        cls._settings = {}

        cls.initialize()

    #
    # Getter
    #
    @classmethod
    def get(
        cls,
        key: str,
        default: Any = None
    ) -> Any:
        """
        設定値を取得する。

        ドット区切りのキーに対応する。

        Args:
            key:
                設定キー。
                例: "database.path"

            default:
                キーが存在しない場合のデフォルト値。

        Returns:
            Any:
                設定値。
                キーが存在しない場合は default を返す。
        """

        cls._ensure_initialized()

        value: Any = cls._settings

        for part in key.split("."):

            if not isinstance(value, dict):
                return default

            if part not in value:
                return default

            value = value[part]

        return value

    @classmethod
    def get_env(
        cls,
        key: str,
        default: str | None = None
    ) -> str | None:
        """
        環境変数を取得する。

        Args:
            key:
                環境変数名。

            default:
                環境変数が存在しない場合のデフォルト値。

        Returns:
            str | None:
                環境変数の値。
        """

        cls._ensure_initialized()

        return getenv(key, default)

    @classmethod
    def get_str(
        cls,
        key: str,
        default: str = ""
    ) -> str:
        """
        文字列型の設定値を取得する。

        Raises:
            TypeError:
                設定値が文字列型ではない場合。
        """

        value = cls.get(key, default)

        if not isinstance(value, str):
            raise TypeError(
                f'Configuration "{key}" must be a string.'
            )

        return value

    @classmethod
    def get_int(
        cls,
        key: str,
        default: int = 0
    ) -> int:
        """
        整数型の設定値を取得する。

        Raises:
            TypeError:
                設定値が整数型ではない場合。
        """

        value = cls.get(key, default)

        if not isinstance(value, int):
            raise TypeError(
                f'Configuration "{key}" must be an integer.'
            )

        return value

    @classmethod
    def get_float(
        cls,
        key: str,
        default: float = 0.0
    ) -> float:
        """
        浮動小数点型の設定値を取得する。

        Raises:
            TypeError:
                設定値が浮動小数点型ではない場合。
        """

        value = cls.get(key, default)

        if not isinstance(value, float):
            raise TypeError(
                f'Configuration "{key}" must be a float.'
            )

        return value

    @classmethod
    def get_bool(
        cls,
        key: str,
        default: bool = False
    ) -> bool:
        """
        真偽値型の設定値を取得する。

        Raises:
            TypeError:
                設定値が真偽値型ではない場合。
        """

        value = cls.get(key, default)

        if not isinstance(value, bool):
            raise TypeError(
                f'Configuration "{key}" must be a bool.'
            )

        return value

    @classmethod
    def get_list(
        cls,
        key: str,
        default: list[Any] | None = None
    ) -> list[Any]:
        """
        リスト型の設定値を取得する。

        Raises:
            TypeError:
                設定値がリスト型ではない場合。
        """

        if default is None:
            default = []

        value = cls.get(key, default)

        if not isinstance(value, list):
            raise TypeError(
                f'Configuration "{key}" must be a list.'
            )

        return value

    @classmethod
    def get_dict(
        cls,
        key: str,
        default: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        辞書型の設定値を取得する。

        Raises:
            TypeError:
                設定値が辞書型ではない場合。
        """

        if default is None:
            default = {}

        value = cls.get(key, default)

        if not isinstance(value, dict):
            raise TypeError(
                f'Configuration "{key}" must be a dictionary.'
            )

        return value

    @classmethod
    def get_path(
        cls,
        key: str,
        default: str | Path = "."
    ) -> Path:
        """
        pathlib.Path型の設定値を取得する。

        Returns:
            Path:
                絶対パスへ変換されたPathオブジェクト。
        """

        value = cls.get(key, default)

        if not isinstance(value, (str, Path)):
            raise TypeError(
                f'Configuration "{key}" must be a path.'
            )

        path = Path(value).expanduser()

        if not path.is_absolute():
            path = cls._PROJECT_ROOT / path

        return path.resolve(strict=False)

    #
    # State
    #
    @classmethod
    def is_initialized(cls) -> bool:
        """
        ConfigManagerが初期化済みか判定する。

        Returns:
            bool:
                初期化済みならTrue。
        """

        return cls._initialized
    
    #
    # Internal
    #
    @classmethod
    def _ensure_initialized(cls) -> None:
        """
        ConfigManagerが初期化済みであることを確認する。

        Raises:
            RuntimeError:
                ConfigManagerが初期化されていない場合。
        """
        if not cls._initialized:
            raise RuntimeError(
                "ConfigManager has not been initialized."
            )
    
