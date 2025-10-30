from datetime import date, timedelta
from collections import defaultdict

# ===== サンプル入力 =====
employees = [
    {"name": "役職者A", "role": "役職者"}, {"name": "役職者B", "role": "役職者"},
    {"name": "一般C", "role": "一般"}, {"name": "一般D", "role": "一般"}, {"name": "一般E", "role": "一般"}
]
target_year = 2025
target_month = 11
unavailable_days = {
    "役職者A": [1, 15],
    "一般C": [8, 9]
}
# =======================

def weekend_days(year: int, month: int):
    """指定年月の土日の日付(dateオブジェクト)をリストで返す"""
    d = date(year, month, 1)
    # 翌月初日を求める
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    days = []
    while d < next_month:
        if d.weekday() in (5, 6):  # 5=土, 6=日
            days.append(d)
        d += timedelta(days=1)
    return days

def build_shift(employees, year, month, unavailable_days):
    # 名称→役割辞書
    roles = {e["name"]: e["role"] for e in employees}
    managers = [e["name"] for e in employees if e["role"] == "役職者"]
    members  = [e["name"] for e in employees]  # 全員

    # 出勤回数カウンタ（均等化のため）
    assigned_count = defaultdict(int)

    # 結果を格納
    shift = {}

    for d in weekend_days(year, month):
        day = d.day

        # その日に出られない人を除外
        def is_available(name):
            return day not in set(unavailable_days.get(name, []))

        available_managers = [m for m in managers if is_available(m)]
        available_all = [m for m in members if is_available(m)]

        # ルールチェック：役職者が最低1名必要
        if not available_managers:
            raise ValueError(f"{d} は出勤可能な役職者がいないため編成できません。")

        # まず役職者から、現在の割当が最も少ない人を1名
        manager_pick = min(available_managers, key=lambda n: assigned_count[n])

        # 残り1名（合計2名にする）。役職者or一般どちらでもOKだが、同じ人は重複不可
        candidates_for_second = [n for n in available_all if n != manager_pick]
        if not candidates_for_second:
            raise ValueError(f"{d} は2人目の要員が確保できません。")

        second_pick = min(candidates_for_second, key=lambda n: assigned_count[n])

        # 本日のシフト決定（必要最低限の2名）
        shift[d.isoformat()] = [manager_pick, second_pick]

        # カウンタ更新
        assigned_count[manager_pick] += 1
        assigned_count[second_pick] += 1

    return shift

if __name__ == "__main__":
    shift = build_shift(employees, target_year, target_month, unavailable_days)
    print(shift)
