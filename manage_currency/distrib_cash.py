import math
from django.db.models import Q
from django.db import models
from .models import (
    AllCash,
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
        rank_sum += (i + 1) * same_rank_players.count()
    print("rank_sum", rank_sum)
    print(all_cash)
    unit = all_cash / rank_sum
    print("unit", unit)
    wallet_list = []
    for j, score in enumerate(score_set):
        same_rank_players = Member.objects.filter(group__score=score)
        for same_rank_player in same_rank_players:
            # 配布DeC量
            cash = (j + 1) * unit
            wallet, _ = Wallet.objects.get_or_create(
                user=same_rank_player,
                defaults={
                    "user": same_rank_player,
                    "cash": 0,
                },
            )
            wallet.cash = math.floor(cash)
            wallet_list.append(wallet)
    print(wallet_list)
    Wallet.objects.bulk_update(wallet_list, fields=["cash"])
    # 合計キャッシュをデータベースに反映
    all_cash_instances = AllCash.objects.all()
    for instance in all_cash_instances:
        instance.all_cash = Wallet.objects.aggregate(models.Sum("cash"))["cash__sum"]
        instance.save()


# いらないかも
# #チーム所属なしの人間にcash配布
# def give_cash_to_stray_people():
#     pass
