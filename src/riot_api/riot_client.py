"""
riot_client.py

Riot APIとの通信を管理するモジュール。

本モジュールはRiot APIへのHTTP通信を提供する。

単独実行した場合は、Riot APIとの疎通確認を行う。
"""

from __future__ import annotations

from typing import Any

import requests

from src.configuration.config_manager import ConfigManager
from src.common.log_manager import LogManager


class RiotClient:
    """
    Riot API通信クラス。
    """

    _ACCOUNT_API_URL = (
        "https://asia.api.riotgames.com"
        "/riot/account/v1/accounts/by-riot-id"
    )

    def __init__(self) -> None:
        """
        RiotClientを初期化する。
        """

        self._logger = LogManager.get_logger(__name__)

        self._api_key = ConfigManager.get_env("RIOT_API_KEY")

        if not self._api_key:
            raise RuntimeError(
                "RIOT_API_KEY is not configured."
            )

    def get_account(
        self,
        game_name: str,
        tag_line: str
    ) -> dict[str, Any]:
        """
        Riot IDからアカウント情報を取得する。

        Args:
            game_name:
                Riot IDのゲーム名

            tag_line:
                Riot IDのタグライン

        Returns:
            dict[str, Any]:
                Riot APIから返却されたJSON
        """

        url = (
            f"{self._ACCOUNT_API_URL}"
            f"/{game_name}"
            f"/{tag_line}"
        )

        headers = {
            "X-Riot-Token": self._api_key
        }

        response = requests.get(
            url=url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    @classmethod
    def run_example(cls) -> None:
        """
        Riot APIとの疎通確認を実行する。
        """

        LogManager.initialize()
        ConfigManager.initialize()

        logger = LogManager.get_logger(__name__)

        logger.info("===== Riot API Communication Test =====")

        client = cls()

        game_name = ConfigManager.get_env("RIOT_GAME_NAME")

        tag_line = ConfigManager.get_env("RIOT_TAG_LINE")

        if not game_name:
            raise ValueError("RIOT_GAME_NAME is not set.")

        if not tag_line:
            raise ValueError("RIOT_TAG_LINE is not set.")

        account = client.get_account(
            game_name=game_name,
            tag_line=tag_line
        )

        logger.info(
            "Connected successfully."
        )

        logger.info(
            "Game Name : %s",
            account["gameName"]
        )

        logger.info(
            "Tag Line  : %s",
            account["tagLine"]
        )

        logger.info(
            "PUUID     : %s",
            account["puuid"]
        )


if __name__ == "__main__":
    RiotClient.run_example()