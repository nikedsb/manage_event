from django.db.models import Q
from .models import (
    Member,
    Team,
    Wallet,
    Star,
    Product,
    Purchase,
    Transaction,
    Answer,
    Quiz,
    QuizOption,
    FinishedQuiz,
)

# 単位ランク当たりのDeC計算と配布
def calc_and_distrib_cash():
    players = (
        Member.objects.select_related("group")
        .filter(is_present=True)
        .exclude(Q(is_superuser=True) | Q(group__isnull=True))
    )
    # 全てのDeCを計算
    all_cash = players.count() * 550
    # 何種類のスコアがあるか
    score_list = []
    for player in players:
        score_list.append(player.group.score)
    # 小さい順に並べる
    score_set = sorted(set(score_list))
    # ランク合計を求める(順位で重み付けするため)
    rank_sum = 0
    for i, score in enumerate(score_set):
        same_rank_players = Member.objects.filter(group__score=score)
        # 重み付けの比率部分→適宜調整
        rank_sum += (i + 1) * same_rank_players.count() / 2

        # 最終ループの時
        if i + 1 == len(score_set):
            print(rank_sum)
            # 単位rank当たりのDeC計算
            unit = all_cash / rank_sum
            # bulk_update用
            wallet_list = []
            for same_rank_player in same_rank_players:
                cash = (i + 1) * unit
                wallet, _ = Wallet.objects.get_or_create(
                    user=same_rank_player,
                    defaults={
                        "user": same_rank_player,
                        "cash": 0,
                    },
                )
                wallet.cash = cash
                wallet_list.append(wallet)
            Wallet.objects.bulk_update(wallet_list)


# いらないかも
# #チーム所属なしの人間にcash配布
# def give_cash_to_stray_people():
#     pass
