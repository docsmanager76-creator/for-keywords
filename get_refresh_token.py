"""One-time helper: turn an OAuth client into a Google Ads refresh token.

Run this on YOUR OWN computer, not in a Claude session -- it opens a
browser for the Google consent screen, and no browser exists in the
remote container.

    pip install google-auth-oauthlib
    python3 get_refresh_token.py

It asks for the client ID and secret rather than reading them from a file,
so no credential ever lands on disk or in git. Paste the refresh token it
prints straight into your environment settings.

Prerequisites, both easy to miss:
  - the OAuth client must be of type "Desktop app"
  - your own Google account must be listed under Test users on the
    OAuth consent screen, or Google answers with "Access blocked"
"""
import getpass, sys

SCOPES = ["https://www.googleapis.com/auth/adwords"]


def main():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install google-auth-oauthlib")

    client_id = input("Client ID: ").strip()
    client_secret = getpass.getpass("Client secret (hidden): ").strip()
    if not client_id or not client_secret:
        sys.exit("Both values are required.")

    flow = InstalledAppFlow.from_client_config(
        {"installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }},
        scopes=SCOPES,
    )

    # access_type=offline and prompt=consent together are what make Google
    # hand back a refresh token. Without them a re-authorization returns
    # only a short-lived access token and the script prints nothing useful.
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    if not creds.refresh_token:
        sys.exit("No refresh token returned. Revoke the app's access at "
                 "https://myaccount.google.com/permissions and run this again.")

    print("\nGOOGLE_ADS_REFRESH_TOKEN =", creds.refresh_token)
    print("\nStore it in your environment settings. Do not commit it.")


if __name__ == "__main__":
    main()
