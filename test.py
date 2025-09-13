from python_access.crud_methods.auth_crud import get_all, get_by_id, create, delete_by_id

print("All Users:")
all_users = get_all()
for user in all_users:
    print(user)
print("\n")

print("Get User by ID (1):")
print(get_by_id(1))
print("\n")

print("Create New User:")
new_user = create("new_firebase_id", "new_email", "new_username")
print(new_user)
print("\n")

print("Delete User by ID (1):")
delete_by_id(1)
print("User with ID 1 deleted.")
print("\n")


