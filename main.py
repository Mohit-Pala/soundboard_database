import argparse
import sys
import json
from python_access.crud_methods import auth_crud, sound_crud
from python_access.errors.exceptions import NotFoundError, DeleteError, CreateError

def convert_to_serializable(obj):
    """Convert pandas/numpy types to JSON serializable Python types"""
    if hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            if hasattr(value, 'item'):  # numpy types
                result[key] = value.item()
            else:
                result[key] = value
        return result
    return obj

def create_parser():
    parser = argparse.ArgumentParser(description='Sound Board Database CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Auth subcommands
    auth_parser = subparsers.add_parser('auth', help='Authentication management')
    auth_subparsers = auth_parser.add_subparsers(dest='auth_action', help='Auth actions')

    auth_subparsers.add_parser('get_all', help='Get all auth records')

    get_by_id_parser = auth_subparsers.add_parser('get_by_id', help='Get auth record by ID')
    get_by_id_parser.add_argument('--id', type=int, required=True, help='Auth record ID')

    delete_by_id_parser = auth_subparsers.add_parser('delete_by_id', help='Delete auth record by ID')
    delete_by_id_parser.add_argument('--id', type=int, required=True, help='Auth record ID')

    create_auth_parser = auth_subparsers.add_parser('create', help='Create new auth record')
    create_auth_parser.add_argument('--firebase_id', required=True, help='Firebase ID')
    create_auth_parser.add_argument('--email', required=True, help='Email address')
    create_auth_parser.add_argument('--username', required=True, help='Username')

    # Sound subcommands
    sound_parser = subparsers.add_parser('sound', help='Sound management')
    sound_subparsers = sound_parser.add_subparsers(dest='sound_action', help='Sound actions')

    sound_subparsers.add_parser('get_all', help='Get all sound records')

    sound_get_by_id_parser = sound_subparsers.add_parser('get_by_id', help='Get sound record by ID')
    sound_get_by_id_parser.add_argument('--id', type=int, required=True, help='Sound record ID')

    sound_delete_by_id_parser = sound_subparsers.add_parser('delete_by_id', help='Delete sound record by ID')
    sound_delete_by_id_parser.add_argument('--id', type=int, required=True, help='Sound record ID')

    create_sound_parser = sound_subparsers.add_parser('create', help='Create new sound record')
    create_sound_parser.add_argument('--user_id', type=int, required=True, help='User ID')
    create_sound_parser.add_argument('--sound_name', required=True, help='Sound name')
    create_sound_parser.add_argument('--description', required=True, help='Sound description')
    create_sound_parser.add_argument('--sound_path', required=True, help='Sound file path')
    create_sound_parser.add_argument('--time', type=int, required=True, help='Sound duration in seconds')

    return parser

def handle_auth_commands(args):
    try:
        if args.auth_action == 'get_all':
            auths = auth_crud.get_all()
            result = [convert_to_serializable(auth) for auth in auths]
            print(json.dumps({"success": True, "data": result}))
        elif args.auth_action == 'get_by_id':
            auth = auth_crud.get_by_id(args.id)
            print(json.dumps({"success": True, "data": convert_to_serializable(auth)}))
        elif args.auth_action == 'delete_by_id':
            auth_crud.delete_by_id(args.id)
            print(json.dumps({"success": True, "message": f"Auth record with ID {args.id} deleted successfully"}))
        elif args.auth_action == 'create':
            auth = auth_crud.create(args.firebase_id, args.email, args.username)
            print(json.dumps({"success": True, "data": convert_to_serializable(auth)}))
    except (NotFoundError, DeleteError, CreateError) as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

def handle_sound_commands(args):
    try:
        if args.sound_action == 'get_all':
            sounds = sound_crud.get_all()
            result = [convert_to_serializable(sound) for sound in sounds]
            print(json.dumps({"success": True, "data": result}))
        elif args.sound_action == 'get_by_id':
            sound = sound_crud.get_by_id(args.id)
            print(json.dumps({"success": True, "data": convert_to_serializable(sound)}))
        elif args.sound_action == 'delete_by_id':
            sound_crud.delete_by_id(args.id)
            print(json.dumps({"success": True, "message": f"Sound record with ID {args.id} deleted successfully"}))
        elif args.sound_action == 'create':
            sound = sound_crud.create(args.user_id, args.sound_name, args.description, args.sound_path, args.time)
            print(json.dumps({"success": True, "data": convert_to_serializable(sound)}))
    except (NotFoundError, DeleteError, CreateError) as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

def main():
    parser = create_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.command == 'auth':
        if not args.auth_action:
            parser.parse_args(['auth', '--help'])
        else:
            handle_auth_commands(args)
    elif args.command == 'sound':
        if not args.sound_action:
            parser.parse_args(['sound', '--help'])
        else:
            handle_sound_commands(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()