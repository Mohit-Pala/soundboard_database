from python_access.models.auth_model import AuthModel
from python_access.models.sound_model import SoundModel

from python_access.crud_methods.auth_crud import get_all as get_all_auths
from python_access.crud_methods.auth_crud import get_by_id as get_auth_by_id
from python_access.crud_methods.auth_crud import create as create_auth
from python_access.crud_methods.auth_crud import delete_by_id as delete_auth_by_id

from python_access.crud_methods.sound_crud import get_all as get_all_sounds
from python_access.crud_methods.sound_crud import get_by_id as get_sound_by_id
from python_access.crud_methods.sound_crud import create as create_sound
from python_access.crud_methods.sound_crud import delete_by_id as delete_sound_by_id
