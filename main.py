from src.configuration.config_manager import ConfigManager
from src.common.log_manager import LogManager
from src.riot_api.riot_client import RiotClient
from src.setup.initializer import (
    Initializer,
    InitializeMode,
)


def main() -> None:

    try:

        #
        # 初期設定
        #
        initializer = Initializer(
            mode=InitializeMode.INTERACTIVE
        )
        initializer.run()

        #
        # ConfigManager
        #
        ConfigManager.initialize()

        #
        # LogManager
        #
        LogManager.initialize()
        logger = LogManager.get_logger(__name__)

        logger.info("ConfigManager initialized successfully.")
        logger.info("Application started.")

        #
        # Riot API Communication Test
        #
        client = RiotClient()

        game_name = ConfigManager.get_env("RIOT_GAME_NAME")
        tag_line = ConfigManager.get_env("RIOT_TAG_LINE")

        if not game_name:
            raise ValueError("RIOT_GAME_NAME is not configured.")

        if not tag_line:
            raise ValueError("RIOT_TAG_LINE is not configured.")

        account = client.get_account(
            game_name=game_name,
            tag_line=tag_line,
        )

        logger.info("Riot API communication succeeded.")

        logger.info(
            "Account Information:\n"
            "  Game Name : %s\n"
            "  Tag Line  : %s\n"
            "  PUUID     : %s",
            account["gameName"],
            account["tagLine"],
            account["puuid"],
        )


        #
        # TODO
        #
        database_path = ConfigManager.get_path(
            "database.path"
        )

        logger.info(
            "Database path: %s",
            database_path
        )

        logger.info("Application terminated successfully.")

    except Exception:

        #
        # 初期化後のみログ出力
        #
        if LogManager.is_initialized():
            logger = LogManager.get_logger(__name__)
            logger.exception("Unexpected error occurred.")

        raise


if __name__ == "__main__":
    main()