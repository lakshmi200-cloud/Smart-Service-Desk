
from application.auth_service import AuthService
from application.request_service import RequestService
from domain.exceptions import (
    AlreadyResolvedError,
    AuthenticationError,
    DuplicateRequestError,
    InvalidPriorityError,
    PersistenceError,
    RequestNotFoundError,
)
from infrastructure.file_repository import FileRepository
from infrastructure.user_repository import UserRepository


def show_request_menu(auth_service):
    print("\n" + "=" * 60)
    print("             SMART SERVICE DESK")
    print("=" * 60)
    print("1. Create New Account")
    print("2. Login")
    print("3. Exit")

    while True:
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            username = input("Create username: ").strip()
            password = input("Create password (minimum 8 characters): ")
            confirm = input("Confirm password: ")

            try:
                auth_service.register(username, password, confirm)
                print("Account created successfully! You can now log in.")
            except AuthenticationError as error:
                print(f"Registration failed: {error}")
            return None

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ")

            try:
                logged_in_user = auth_service.login(username, password)
                print(f"\nLogin successful. Welcome, {logged_in_user}!")
                return logged_in_user
            except AuthenticationError as error:
                print(f"Login failed: {error}")
                return None

        elif choice == "3":
            return "EXIT"

        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


def display_request(request):
    print(f"Request ID       : {request.request_id}")
    print(f"Employee Name    : {request.employee_name}")
    print(f"Issue Description: {request.issue}")
    print(f"Priority         : {request.priority}")
    print(f"Status           : {request.status}")
    print(f"Created At       : {request.created_at}")

    if request.resolved_at:
        print(f"Resolved At      : {request.resolved_at}")


def display_all_requests(requests):
    if not requests:
        print("\nNo service requests found.")
        return

    # Set fixed column widths
    id_width = 15
    employee_width = 22
    issue_width = 32
    priority_width = 15
    status_width = 15

    total_width = (
        id_width + employee_width + issue_width
        + priority_width + status_width
    )

    print("\n")
    print("=" * total_width)
    print(" " * 30 + "ALL SERVICE REQUESTS")
    print("=" * total_width)

    # Table headings
    print(
        f"{'REQUEST ID':<{id_width}}"
        f"{'EMPLOYEE NAME':<{employee_width}}"
        f"{'ISSUE DESCRIPTION':<{issue_width}}"
        f"{'PRIORITY':<{priority_width}}"
        f"{'STATUS':<{status_width}}"
    )

    print("-" * total_width)

    # Table rows
    for item in requests:
        print(
            f"{str(item.request_id):<{id_width}}"
            f"{item.employee_name:<{employee_width}}"
            f"{item.issue:<{issue_width}}"
            f"{item.priority:<{priority_width}}"
            f"{item.status:<{status_width}}"
        )

    print("=" * total_width)


def show_menu():
    print("\n" + "=" * 60)
    print("           SMART SERVICE DESK SYSTEM")
    print("=" * 60)
    print("1. Create Service Request")
    print("2. View All Requests")
    print("3. Search Request")
    print("4. Resolve Request")
    print("5. Exit")
    print("6. Logout")


def run_application():
    try:
        user_repository = UserRepository()
        auth_service = AuthService(user_repository)
        repository = FileRepository()
        request_service = RequestService(repository)

    except (PersistenceError, RuntimeError) as error:
        print(f"Startup error: {error}")
        return

    while True:
        user = show_request_menu(auth_service)

        if user == "EXIT":
            print("Thank you for using Smart Service Desk. Goodbye!")
            return

        if user is None:
            continue

        while True:
            show_menu()
            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    request_id = input("Enter Request ID: ").strip()
                    employee = input("Enter Employee Name: ").strip()
                    issue = input("Enter Issue: ").strip()
                    priority = input(
                        "Enter Priority (LOW/MEDIUM/HIGH): "
                    ).strip()

                    request = request_service.create_request(
                        request_id, employee, issue, priority
                    )

                    print(
                        f"\nService Request '{request.request_id}' "
                        "created successfully."
                    )

                elif choice == "2":
                    requests = request_service.view_requests()
                    display_all_requests(requests)

                elif choice == "3":
                    request_id = input(
                        "Enter Request ID to search: "
                    ).strip()

                    display_request(
                        request_service.search_request(request_id)
                    )

                elif choice == "4":
                    request_id = input(
                        "Enter Request ID to resolve: "
                    ).strip()

                    request = request_service.resolve_request(request_id)

                    print(
                        f"Request '{request.request_id}' "
                        "has been marked RESOLVED."
                    )

                elif choice == "5":
                    print(
                        "Thank you for using Smart Service Desk. Goodbye!"
                    )
                    return

                elif choice == "6":
                    print(f"\n{user} has been logged out.")
                    break

                else:
                    print(
                        "Invalid menu choice. "
                        "Please enter a number from 1 to 6."
                    )

            except (
                DuplicateRequestError,
                RequestNotFoundError,
                InvalidPriorityError,
                AlreadyResolvedError,
                PersistenceError,
                ValueError,
            ) as error:
                print(f"Error: {error}")


if __name__ == "__main__":
    run_application()
