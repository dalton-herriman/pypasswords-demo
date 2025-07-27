from cli.register import register
from cli.login import login


def main():
    print("1) Register")
    print("2) Login")
    choice = input("Choose an option: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
