"""
A script that outputs the names of the Chicago Bulls players for the 2025-26 season
- Uses nba_api
- Team abbreviation: CHI
- Includes error handling
"""

from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from requests.exceptions import RequestException
import pandas as pd


SEASON = "2025-26"   # Official NBA Season Parameter Format
TEAM_ABBR = "CHI"    # Chicago Bulls


def get_team_id(team_abbr: str) -> int:
    """Get team_id from team abbreviation (e.g., CHI). Raise an error if not found."""
    all_teams = teams.get_teams()
    for t in all_teams:
        if t.get("abbreviation") == team_abbr:
            return t["id"]
    raise ValueError(f"Team not found for abbreviation: {team_abbr}")


def fetch_team_roster(team_id: int, season: str) -> pd.DataFrame:
    """
    Fetch the roster information for a specified team and season.
    Raise an exception if the fetch fails.
    """
    try:
        roster = commonteamroster.CommonTeamRoster(
            team_id=team_id,
            season=season,
            timeout=60,
        )
        df = roster.get_data_frames()[0]
        return df
    except RequestException as e:
        print("[ERROR] HTTP level error occurred:", e)
        raise
    except Exception as e:
        print("[ERROR] Unexpected error occurred while fetching roster:", e)
        raise


def main():
    try:
        team_id = get_team_id(TEAM_ABBR)
        print(f"Team: {TEAM_ABBR}, team_id: {team_id}")
    except Exception as e:
        print("[ERROR] Failed to get team ID:", e)
        return

    try:
        df_roster = fetch_team_roster(team_id, SEASON)
    except Exception:
        # Since the error message has already been displayed, just exit
        return

    if df_roster.empty:
        print(f"[INFO] {SEASON} season roster information could not be fetched.")
        return

    # Column name inspection (for debugging)
    # print(df_roster.columns.tolist())

    # Most cases have "PLAYER" column with player names
    column_candidates = ["PLAYER", "PLAYER_NAME"]
    player_col = None
    for c in column_candidates:
        if c in df_roster.columns:
            player_col = c
            break

    if player_col is None:
        print("[ERROR] Player name column not found. Column information:", df_roster.columns.tolist())
        return

    print(f"\n=== Chicago Bulls Roster ({SEASON}) ===")
    for name in df_roster[player_col]:
        print(name)


if __name__ == "__main__":
    main()
