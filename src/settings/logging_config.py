import json
import logging

json_formatter = logging.Formatter(
    json.dumps(
        {
            "time": "%(asctime)s.%(msecs)03d",
            "level": "%(levelname)-6s",
            "funcName": "%(funcName)s()",
            "line": "%(pathname)s:%(lineno)d",
            "loggerName": "%(name)s",
            "message": "%(message)s",
        },
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)

handler = logging.StreamHandler()
handler.setFormatter(json_formatter)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
