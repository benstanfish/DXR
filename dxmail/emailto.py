import webbrowser
import urllib.parse

def open_default_email(to_list, cc_list=None, subject="", body=""):

    if not to_list:
        raise ValueError("At least one recipient is required.")

    to_str = "; ".join(to_list)
    cc_str = "; ".join(cc_list) if cc_list else ""

    params = {}
    if cc_str:
        params["cc"] = cc_str
    if subject:
        params["subject"] = subject
    if body:
        params["body"] = body

    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    mailto_url = f"mailto:{to_str}?{query}" if query else f"mailto:{to_str}"

    try:
        webbrowser.open(mailto_url)
    except Exception as e:
        print(f'{e}')
