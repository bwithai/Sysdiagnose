import os

from fastapi import APIRouter
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse

from iShutdown_KasperskyLab.iShutdown_detect import detect_sys_diagnose
from iShutdown_KasperskyLab.iShutdown_stats import get_log_stats
from utils import get_target_file, parse_shutdown, convert_csv_to_html

extract_router = APIRouter(prefix="", tags=["Extract tar.gz files"])


@extract_router.get("/extract-data/")
async def extract_upload_file():
    tar_file_dir = os.path.join(os.getcwd(), "storage")
    tar_file_path = get_target_file(tar_file_dir, "tar.gz")
    if not tar_file_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=".tar.gz file not found")

    logfile_dir = os.path.join(os.getcwd(), "storage/parse_shutdown")
    logfile = get_target_file(logfile_dir, ".log")
    if not logfile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=".log file not found")

    # call iShutdown_detect.py
    summary_response = detect_sys_diagnose(tar_file_path)
    # call iShutdown_stats.py
    restart_stats_response = get_log_stats(logfile)
    # stats
    log_lines, txt_lines, csv_lines = parse_shutdown()

    extract_data = {
        "summary": summary_response,
        "restart_data": restart_stats_response,
        "log_file": log_lines,
        "extraction_summary": txt_lines,
        "parse_shutdown_csv": csv_lines

    }

    return JSONResponse(content=extract_data)


@extract_router.get("/csv-to-html")
async def csv_to_html():
    html_table = convert_csv_to_html()
    return HTMLResponse(content=html_table)
