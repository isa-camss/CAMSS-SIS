import com.nttdata.dgi.util.io as io

HEADERS = {"failed": "FAILED", "success": "SUCCESS", "error": "ERROR", "warning": "WARNING"}

FILE_NOT_FOUND = {"id": 1, "header": HEADERS.get('failed'), "message": f"The file %s does not exist", "action": "Review the configuration.", "code": 404}
MULTIPLE_ELEMENTS_PER_LINE = {"id": 2, "header": HEADERS.get('failed'), "message": f"The line %s contains multiple elements.", "action": "Preprocess the file?", "code": 404}


def dt() -> str:
    return 'now: ' + str(io.now())


def error(error_details: dict, arguments: tuple, date_time_info: bool = True, action: bool = True):
    return io.log(f'{error_details.get("header")} '
                  f'({str(error_details.get("code"))}): '
                  f'{error_details.get("message") % arguments} '
                  f'{error_details.get("action") if action else ""}'
                  f'({dt() if date_time_info else ""}).')
