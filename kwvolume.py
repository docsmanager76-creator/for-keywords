"""Check keyword demand against Google Keyword Planner.

Returns the three columns the Keyword Planner UI shows -- avg monthly
searches, three month change, YoY change -- as TSV, one row per keyword.
Only the first is an API field; the other two are derived here from the
monthly volume series, because the API does not expose them directly.

    python3 kwvolume.py "best card scraper" "best marking knife"
    python3 kwvolume.py --check          # verify credentials only

Reads five values from the environment (see README section in this file's
docstring at the bottom). Needs: pip install google-ads
"""
import datetime, os, sys

# Google reports whole-month data only, and the most recent month lags, so
# every window ends at the last completed month. 15 months back gives the
# 13 points a YoY comparison needs plus slack for a missing tail month.
WINDOW_MONTHS = 15
LANGUAGE_ENGLISH = "languageConstants/1000"
GEO_UNITED_STATES = "geoTargetConstants/2840"

MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY",
          "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

REQUIRED = ["GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_ADS_CLIENT_ID",
            "GOOGLE_ADS_CLIENT_SECRET", "GOOGLE_ADS_REFRESH_TOKEN",
            "GOOGLE_ADS_LOGIN_CUSTOMER_ID"]


def build_client():
    missing = [k for k in REQUIRED if not os.environ.get(k)]
    if missing:
        sys.exit("Missing environment variables:\n  " + "\n  ".join(missing))
    from google.ads.googleads.client import GoogleAdsClient
    return GoogleAdsClient.load_from_dict({
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "login_customer_id": os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"].replace("-", ""),
        "use_proto_plus": True,
    })


def window():
    """(start_year, start_month, end_year, end_month) of the lookback range."""
    today = datetime.date.today()
    end = datetime.date(today.year, today.month, 1) - datetime.timedelta(days=1)
    total = end.year * 12 + (end.month - 1) - (WINDOW_MONTHS - 1)
    return total // 12, total % 12 + 1, end.year, end.month


def fetch(client, keywords):
    svc = client.get_service("KeywordPlanIdeaService")
    req = client.get_type("GenerateKeywordHistoricalMetricsRequest")
    req.customer_id = (os.environ.get("GOOGLE_ADS_CUSTOMER_ID")
                       or os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"]).replace("-", "")
    req.keywords.extend(keywords)
    req.language = LANGUAGE_ENGLISH
    req.geo_target_constants.append(GEO_UNITED_STATES)
    req.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH

    sy, sm, ey, em = window()
    rng = req.historical_metrics_options.year_month_range
    rng.start.year, rng.end.year = sy, ey
    rng.start.month = client.enums.MonthOfYearEnum[MONTHS[sm - 1]]
    rng.end.month = client.enums.MonthOfYearEnum[MONTHS[em - 1]]

    return svc.generate_keyword_historical_metrics(request=req)


def series(metrics):
    """Monthly volumes oldest-first, so [-1] is the most recent month."""
    def key(v):
        name = v.month.name if hasattr(v.month, "name") else str(v.month)
        return (v.year, MONTHS.index(name) if name in MONTHS else 0)
    return [v.monthly_searches or 0 for v in sorted(metrics.monthly_search_volumes, key=key)]


def change(vals, lag):
    """Percent change between the newest month and `lag` months earlier."""
    if len(vals) <= lag:
        return None
    now, then = vals[-1], vals[-1 - lag]
    if not then:
        return None
    return (now - then) / then * 100.0


def verdict(avg):
    """The routine wants proven-but-not-saturated demand."""
    if avg is None:
        return "NO DATA"
    if avg < 300:
        return "TOO LOW"
    if avg > 60000:
        return "TOO BIG"
    return "MEDIUM"


def fmt(pct, avg):
    # Percent swings on a tiny base are noise: 5 searches to 50 reads as
    # +900% and means nothing. Withhold the number rather than mislead.
    if pct is None:
        return "n/a"
    if avg is not None and avg < 1000:
        return "n/a (base too small)"
    return f"{pct:+.0f}%"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    client = build_client()

    if "--check" in sys.argv:
        fetch(client, ["cordless drill"])
        print("OK - credentials work and the API answered.")
        return
    if not args:
        sys.exit(__doc__)

    print("keyword\tavg_monthly_searches\tthree_month_change\tyoy_change\tcompetition\tverdict")
    for res in fetch(client, args).results:
        m = res.keyword_metrics
        avg = m.avg_monthly_searches
        vals = series(m)
        comp = m.competition.name if hasattr(m.competition, "name") else str(m.competition)
        print("\t".join([res.text, str(avg if avg is not None else "n/a"),
                         fmt(change(vals, 3), avg), fmt(change(vals, 12), avg),
                         comp, verdict(avg)]))


if __name__ == "__main__":
    main()
