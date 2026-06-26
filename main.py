from src.configuration.config_manager import ConfigManager
from src.common.log_manager import LogManager
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