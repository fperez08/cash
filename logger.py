from datetime import datetime
from pathlib import Path
import logging


def setup_global_logging(
    log_dir: str = "logs",
    loggers=[
        logging.getLogger("__main__"),
        logging.getLogger(__package__),
    ],
    level=logging.INFO,
    global_level=None,
    stream_level=logging.INFO,
):
    """Set up basic logging to stderr and a log directory

    loggers: defaults to this module's logger and this module's package's logger
    level: set log level for `loggers` (above parameter). Defaults to logging.INFO
    global_level: let log level for loggers in in `loggers`(like 3rd party libs)
    Defaults to logging.ERROR.
    stream_level: set log level of stderr specifically. Defaults to `level`'s value

    See `logging.Logger.manager.loggerDict` for a list of all loggers
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logname = log_dir / datetime.now().strftime("%Y-%m-%d.%H.%M.%S.log")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_level or level)

    logging.basicConfig(
        format="# %(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s\n%(message)s\n",
        level=global_level,  # logging package sets to logging.ERROR if it's None here
        handlers=(stream_handler, logging.FileHandler(logname)),
    )

    if loggers is not None:
        for log in loggers:
            if log is not logging.getLogger():
                log.setLevel(level)
