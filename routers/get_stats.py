import os

from fastapi import APIRouter

from exceptions import not_found_exception
from iShutdown_KasperskyLab.iShutdown_stats import get_log_stats
from utils import get_target_file

stats_router = APIRouter(prefix="", tags=["Reboot stats of a target Shutdown.log"])


@stats_router.get("/log-stats/")
async def get_stats():
    logfile_dir = os.path.join(os.getcwd(), "storage/parse_shutdown")
    logfile = get_target_file(logfile_dir, ".log")
    if not logfile:
        raise not_found_exception

    log_stats = get_log_stats(logfile)

    return {
        "stats": log_stats
    }
