# Google Keyword Planner setup

`kwvolume.py` checks keyword demand against Google Keyword Planner. It needs
five credentials. This file records how to get them, because the two steps in
the middle can only be done by a human with the Google account password.

## What is already done

- Manager (MCC) account: **Microvex, 118-300-2721**
- Developer token: obtained from Google Ads -> Admin -> API Center
- OAuth client ID + secret: obtained from Google Cloud Console

## What still needs a human

### 1. Refresh token

Requires signing in to the Google account and clicking Allow on a consent
screen. No tool, script, or agent can do this — that is the point of the
consent screen.

Easiest route, all in a browser, no terminal:

1. In Cloud Console -> Credentials, edit the OAuth client. It must be type
   **Web application**, and it needs this exact Authorized redirect URI:
   `https://developers.google.com/oauthplayground`
2. Open <https://developers.google.com/oauthplayground>
3. Gear icon (top right):
   - tick **Use your own OAuth credentials**, paste the client ID and secret
   - OAuth flow: **Server-side**
   - Access type: **Offline** — without this Google returns no refresh token
4. Step 1 panel, in the "Input your own scopes" box, enter:
   `https://www.googleapis.com/auth/adwords`
   then **Authorize APIs**, sign in, **Allow**
5. Step 2 panel: **Exchange authorization code for tokens**. Copy the
   **Refresh token**.
6. Back in Cloud Console, remove the playground redirect URI. It has served
   its purpose and should not stay on the client.

Alternative if you prefer a terminal: `get_refresh_token.py` in this repo does
the same thing, but needs a **Desktop app** OAuth client instead, plus
`pip install google-auth-oauthlib`.

### 2. Environment variables

Set these in the Claude Code environment settings, so every scheduled run can
read them. They cannot live in this repo — committing a secret exposes it.

    GOOGLE_ADS_DEVELOPER_TOKEN
    GOOGLE_ADS_CLIENT_ID
    GOOGLE_ADS_CLIENT_SECRET
    GOOGLE_ADS_REFRESH_TOKEN
    GOOGLE_ADS_LOGIN_CUSTOMER_ID = 1183002721

Docs: <https://code.claude.com/docs/en/claude-code-on-the-web>

## Verifying

    pip install google-ads
    python3 kwvolume.py --check
    python3 kwvolume.py "best card scraper" "best marking knife"

## Two things that will look like bugs but are not

**Volume arrives as ranges, not exact numbers.** Keyword Planner only reports
precise figures to accounts running an active campaign with real spend. The
Microvex account has none, so expect buckets like "1K-10K". This is fine for
the routine's purpose: telling medium demand apart from negligible demand does
not need precision.

**No data until Basic Access is approved.** A freshly issued developer token
carries Test Access, which only works against test accounts and returns
nothing for real keywords. Basic Access approval takes anywhere from a few
hours to five business days. Until the approval email arrives, correct setup
still yields empty results.

## Known gap

Percent-change columns are suppressed below a 1,000 search base. On tiny
volumes they are noise — five searches becoming fifty reads as +900% and means
nothing.
