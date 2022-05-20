from tokenize import group

from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Member,
    Team,
)
from .variables import late_leader_name

# チーム数の算出
def culc_team_num(job):
    # チーム数初期化
    team_num = 0
    people_per_team = 0
    # プレイヤー全体の数(遅刻チームのリーダーと管理者は除く)
    players = Member.objects.filter(is_present=True, is_late=False, job=job, group=None).exclude(
        Q(username=late_leader_name) | Q(is_superuser=True)
    )
    players_num = players.count()
    # 雇用中(リーダー候補)の数
    mentors = Member.objects.filter(
        is_present=True, is_late=False, job=job, is_employee=True, group=None
    ).exclude(Q(username=late_leader_name) | Q(is_superuser=True))
    mentors_num = mentors.count()

    team_dict = {
        "job": job,
        "team_num": team_num,
        "people_per_team": people_per_team,
        "players": players,
        "mentors": mentors,
    }

    if players_num <= 0 or mentors_num <= 0:
        return team_dict
    # 　比率の整数除算
    ratio_int = players_num // mentors_num
    print(ratio_int)
    if ratio_int >= 4:
        # メンターにつき人数が多すぎる時→どうしようもないのでそのまま
        # メンターにつき人数がちょうどよかった(4,5人)の時→そのまま
        people_per_team = ratio_int
        team_dict["team_num"] = mentors_num
        team_dict["people_per_team"] = people_per_team
    elif ratio_int <= 3:
        # 1メンターにつき人数が少なすぎる時
        new_ratio_int = ratio_int
        while new_ratio_int < 4:
            # メンター数が1の時は0除算になる
            if mentors_num >= 2:
                mentors_num -= 1
                new_ratio_int = players_num // mentors_num
            else:
                # 極端に数が少ない時→合計が3以下の時
                if mentors_num == 1 and new_ratio_int <= 3:
                    team_dict["team_num"] = 1
                    team_dict["people_per_team"] = new_ratio_int
                break

        people_per_team = new_ratio_int
        team_dict["team_num"] = mentors_num
        team_dict["people_per_team"] = people_per_team

    return team_dict


# offsetとlimitの話ややこしい
def create_team(team_dict):
    all_players = team_dict["players"].order_by("?")
    mentors = team_dict["mentors"].order_by("?")
    team_num = team_dict["team_num"]
    people_per_team = team_dict["people_per_team"]
    print("チーム数", team_num)
    print("１チームの人数", people_per_team)
    # 不正な値の場合は弾く
    if team_num == 0 or people_per_team == 0:
        return None
    # チーム数だけメンターを取得
    leaders = mentors[:team_num]
    print("リーダーは", leaders)
    normal_mentors = None if team_num == mentors.count() else mentors[: team_num : mentors.count()]
    print("非リーダー", normal_mentors)
    if normal_mentors:
        for normal_mentor in normal_mentors:
            # リーダーじゃない人間は雇用フラグを折る
            normal_mentor.is_employee = False
            normal_mentor.save()
    # チーム作成とリーダー自身に登録
    for leader in leaders:
        team, is_created = Team.objects.get_or_create(
            leader=leader,
            defaults={
                "leader": leader,
                "score": 0,
            },
        )
        if is_created:
            leader.group = team
            leader.save()
        else:
            # 作るの二回目の場合はpass
            continue
    # チームが入ってないものだけ取り出す。
    teams = Team.objects.filter(leader__job=team_dict["job"])
    normal_players = all_players.filter(group=None)
    print("チームなし人間", normal_players, normal_players.count())
    for i, team in enumerate(teams):
        members_num = people_per_team - 1
        print("現状の無所属人数", normal_players.count())
        if members_num <= normal_players.count():
            team_members = normal_players[:members_num]
            print(i, team_members)
        else:
            team_members = normal_players[: normal_players.count()]
            print("else", i, team_members)
        for team_member in team_members:
            team_member.group = team
            team_member.save()

    return {
        "no_team_players": normal_players,
        "people_per_team": people_per_team,
    }


def assign_no_team_players(en_no_team_dict, de_no_team_dict):
    if en_no_team_dict == None or de_no_team_dict == None:
        # 二回目以降の処理はnullを返す
        return

    no_team_engineers = en_no_team_dict["no_team_players"]
    no_team_designers = de_no_team_dict["no_team_players"]
    en_teams = Team.objects.filter(leader__job="Engineer").exclude(
        leader__username=late_leader_name
    )
    de_teams = Team.objects.filter(leader__job="Designer")
    if en_no_team_dict["people_per_team"] >= 3 and de_no_team_dict["people_per_team"] >= 3:
        for en_team in en_teams:
            try:
                no_team_engineer = no_team_engineers.first()
                no_team_engineer.group = en_team
                no_team_engineer.save()
                no_team_engineers = no_team_engineers.filter(group=None)
            except:
                break
        for de_team in de_teams:
            try:
                no_team_designer = no_team_designers.first()
                no_team_designer.group = de_team
                no_team_designer.save()
                no_team_designers = no_team_designers.filter(group=None)
            except:
                break

    elif 1 <= en_no_team_dict["people_per_team"] <= 2 and de_no_team_dict["people_per_team"] >= 3:
        # engineerチームは一つしかない
        # engineerの無所属は0人
        de_stray_people = de_no_team_dict["no_team_players"]
        if de_stray_people.exists():
            engineer_team = Team.objects.filter(leader__job="Engineer").first()
            team_members_num = Member.objects.filter(group=engineer_team).count()
            for de_stray_person in de_stray_people:
                print("エンジニアチームの人数は", team_members_num)
                de_stray_person.group = engineer_team
                de_stray_person.save()
                team_members_num += 1
                if team_members_num >= 4:
                    break

            de_not_team_members = Member.objects.filter(group=None, job="Designer").exclude(
                is_superuser=True
            )
            teams = Team.objects.filter(leader__job="Desginer")
            for team in teams:
                try:
                    de_not_team_member = de_not_team_members.first()
                    de_not_team_member.group = team
                    de_not_team_member.save()
                    de_not_team_members = de_not_team_members.filter(group=None)
                except:
                    break

    elif en_no_team_dict["people_per_team"] >= 3 and 1 <= de_no_team_dict["people_per_team"] <= 2:
        # desginerチームは一つしかない。
        # designerの無所属は0人
        en_stray_people = en_no_team_dict["no_team_players"]
        if en_stray_people.exists():
            designer_team = Team.objects.filter(leader__job="Designer").first()
            team_members_num = Member.objects.filter(group=designer_team).count()
            for en_stray_person in en_stray_people:
                print("デザイナーチームの人数は", team_members_num)
                en_stray_person.group = designer_team
                en_stray_person.save()
                team_members_num += 1
                if team_members_num >= 4:
                    break

            en_not_team_members = Member.objects.filter(group=None, job="Engineer").exclude(
                is_superuser=True
            )
            teams = Team.objects.filter(leader__job="Engineer")
            for team in teams:
                try:
                    en_not_team_member = en_not_team_members.first()
                    en_not_team_member.group = team
                    en_not_team_member.save()
                    en_not_team_members = en_not_team_members.filter(group=None)
                except:
                    break


# クイズへの途中参加はできたレベルの遅刻のチーム
def create_late_team():
    late_leader = get_object_or_404(Member, username=late_leader_name)
    late_team, is_created = Team.objects.get_or_create(
        leader=late_leader, defaults={"leader": late_leader, "score": 0}
    )
    if is_created:
        late_leader.group = late_team
        late_leader.save()
        # 雇用メンバーも遅刻する可能性がある、その場合は問答無用で遅刻チームへ。
        late_people = Member.objects.filter(is_present=True, is_late=True)
        if late_people.exists():
            for late_person in late_people:
                late_person.group = late_team
                print(late_person.username)
                late_person.save()
