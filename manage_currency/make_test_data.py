from manage_currency.models import Member


def create_dummy_members(job, num):
    for i in range(1, num):
        Member.objects.create(
            username=f"sample{i}",
            job=job,
            is_present=True,
            is_employee=False,
            password="thisistest",
        )


def main():
    create_dummy_members("Engineer", 30)


if __name__ == "__main__":
    main()
