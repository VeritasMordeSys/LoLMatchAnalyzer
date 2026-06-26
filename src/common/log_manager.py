"""
log_manager.py

アプリケーション全体で使用するログシステムを管理するモジュール。

Python標準ライブラリ ``logging`` の初期化および Logger オブジェクトの
取得機能を提供する。
"""

from pathlib import Path
import logging


class LogManager:
    """
    ログシステム管理クラス。

    本クラスは Python 標準ライブラリ ``logging`` の初期化を担当する。
    アプリケーション全体で一度だけ初期化を実施し、各モジュールは
    :meth:`get_logger` を使用して Logger を取得する。

    本クラスのインスタンス生成は禁止されている。
    """

    #: ログシステムの初期化状態
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        インスタンス生成を禁止する。

        Raises:
            TypeError: インスタンス生成が要求された場合。
        """
        raise TypeError(
            "LogManager cannot be instantiated. "
            "Use LogManager.initialize() and LogManager.get_logger()."
        )

    @classmethod
    def initialize(cls) -> None:
        """
        ログシステムを初期化する。

        初回呼び出し時のみログ設定を行う。
        2回目以降の呼び出しは何も行わない。
        """

        if cls._initialized:
            return

        project_root = Path(__file__).resolve().parents[2]

        log_directory = project_root / "logs"
        log_directory.mkdir(exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        #
        # Console
        #
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        #
        # File
        #
        file_handler = logging.FileHandler(
            log_directory / "application.log",
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        cls._initialized = True

    @classmethod
    def get_logger(cls, module_name: str) -> logging.Logger:
        """
        Logger オブジェクトを取得する。

        Args:
            module_name: 通常は ``__name__`` を指定する。

        Returns:
            logging.Logger: 指定したモジュールに対応する Logger。

        Raises:
            RuntimeError: ログシステムが初期化されていない場合。
        """

        if not cls._initialized:
            raise RuntimeError(
                "LogManager has not been initialized."
            )

        return logging.getLogger(module_name)
    
    @classmethod
    def is_initialized(cls) -> bool:
        """
        ログシステムが初期化済みかを判定する。

        Returns:
            bool: 初期化済みの場合は ``True``、それ以外は ``False``。
        """
        return cls._initialized