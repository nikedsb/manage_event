from manage_currency.models import Member, Wallet, Star


def create_dummy_members(job, num):
    for i in range(1, num):
        Member.objects.create(
            username=f"sample{i}",
            job=job,
            is_present=True,
            is_employee=False,
            password="thisistest",
        )


def create_wallet_and_star():
    players = Member.objects.all().filter(is_present=True).exclude(is_superuser=True)
    wallet_list = []
    star_list = []
    for player in players:
        wallet = Wallet(user=player, cash=0)
        star = Star(user=player, star=3)
        wallet_list.append(wallet)
        star_list.append(star)
    Star.objects.bulk_create(star_list)
    Wallet.objects.bulk_create(wallet_list)


def main():
    create_dummy_members("Engineer", 30)


if __name__ == "__main__":
    main()
