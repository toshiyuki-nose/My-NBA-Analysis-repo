"""
## bulls_roster_2025_26_jp.py
2025-26シーズンのシカゴ・ブルズの選手名を出力するスクリプト
- nba_api を使用
- チーム略称: CHI
- エラーハンドリング付き
"""

from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from requests.exceptions import RequestException
import pandas as pd


SEASON = "2025-26"   # NBA公式のSeasonパラメータ形式
TEAM_ABBR = "CHI"    # シカゴ・ブルズ


def get_team_id(team_abbr: str) -> int:
    """チーム略称（例: CHI）から team_id を取得する。見つからなければ例外。"""
    all_teams = teams.get_teams()
    for t in all_teams:
        if t.get("abbreviation") == team_abbr:
            return t["id"]
    raise ValueError(f"Team not found for abbreviation: {team_abbr}")


def fetch_team_roster(team_id: int, season: str) -> pd.DataFrame:
    """
    指定チーム・シーズンのロスター情報を取得。
    失敗時は例外を投げる。
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
        print("[ERROR] HTTPレベルのエラーが発生しました:", e)
        raise
    except Exception as e:
        print("[ERROR] ロスター取得中に予期せぬエラーが発生しました:", e)
        raise


def main():
    try:
        team_id = get_team_id(TEAM_ABBR)
        print(f"Team: {TEAM_ABBR}, team_id: {team_id}")
    except Exception as e:
        print("[ERROR] チームID取得に失敗しました:", e)
        return

    try:
        df_roster = fetch_team_roster(team_id, SEASON)
    except Exception:
        # すでにエラーメッセージは出しているので、そのまま終了
        return

    if df_roster.empty:
        print(f"[INFO] {SEASON} シーズンのロスター情報が取得できませんでした。")
        return

    # 列名の確認（デバッグ用）
    # print(df_roster.columns.tolist())

    # 多くのケースで "PLAYER" 列に選手名が入っている
    column_candidates = ["PLAYER", "PLAYER_NAME"]
    player_col = None
    for c in column_candidates:
        if c in df_roster.columns:
            player_col = c
            break

    if player_col is None:
        print("[ERROR] 選手名の列が見つかりませんでした。列情報:", df_roster.columns.tolist())
        return

    print(f"\n=== Chicago Bulls Roster ({SEASON}) ===")
    for name in df_roster[player_col]:
        print(name)


if __name__ == "__main__":
    main()
