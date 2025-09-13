from python_access.models.auth_model import AuthModel
from python_access.errors.exceptions import NotFoundError, DeleteError, CreateError
from config import AUTH_FILE_PATH

import pandas as pd

def read_auth_file() -> pd.DataFrame:
    df = pd.read_csv(AUTH_FILE_PATH)
    return df

def get_all() -> list[AuthModel]:
    df = read_auth_file()
    auths = [AuthModel(**row) for index, row in df.iterrows()]
    if not auths:
        raise NotFoundError("No users found")
    return auths

def get_by_id(id: int) -> AuthModel:
    df = read_auth_file()
    user_row = df[df['Id'] == id]
    if user_row.empty:
        raise NotFoundError(f"User with Id {id} not found")
    return AuthModel(**user_row.iloc[0])

def delete_by_id(id: int) -> None:
    df = read_auth_file()
    if id not in df['Id'].values:
        raise NotFoundError(f"User with Id {id} not found")
    df = df[df['Id'] != id]
    try:
        df.to_csv(AUTH_FILE_PATH, index=False)
    except Exception as e:
        raise DeleteError(f"Failed to delete user with Id {id}: {e}")
    return None
    
def create(firebase_id: str, email: str, username: str) -> AuthModel:
    df = read_auth_file()
    new_id = df['Id'].max() + 1 if not df.empty else 1
    new_user = AuthModel(Id=new_id, FirebaseId=firebase_id, Email=email, Username=username)
    df = pd.concat([df, pd.DataFrame([new_user.__dict__])], ignore_index=True)
    try:
        df.to_csv(AUTH_FILE_PATH, index=False)
    except Exception as e:
        raise CreateError(f"Failed to create user: {e}")
    return new_user