from ATS_v5.main import bridge


code = """

web.get'https://youtube.com' then status=web.get+status_code;
if status?'200' { print:'YouTube OK'* print:status* };
if status!'200' { print:'YouTube failed'* print:status* };


web.get'https://google.com' then status=web.get+status_code;
if status?'200' { print:'Google OK'* print:status* };
if status!'200' { print:'Google failed'* print:status* };

web.get'https://steamidfinder.com' then status=web.get+status_code;
if status?'200' { print:'SteamIDFinder OK'* print:status* };
if status!'200' { print:'SteamIDFinder failed'* print:status* };
"""

bridge(code, {})