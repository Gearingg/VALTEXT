import os
import glob
import re
import shutil
import subprocess
import sys
from pathlib import Path
from time import sleep

# Set debug to True for additional print statements
welcome_displayed = True
debug_mode = False

# Script Variables
script_version = '1.0'

update_available = False
updating_game = False
update_completed = False
game_updated = False

last_read_position = 0

# Game Variables
RIOT_GAMES_ROOT_FOLDER = Path('D:/Riot Games').resolve()
RIOT_CLIENT_ROOT_FOLDER = (RIOT_GAMES_ROOT_FOLDER / 'Riot Client').resolve()
RIOT_CLIENT_EXE = (RIOT_CLIENT_ROOT_FOLDER / 'RiotClientServices.exe').resolve()

VALORANT_ROOT_FOLDER = (RIOT_GAMES_ROOT_FOLDER / 'VALORANT').resolve()
VALORANT_EXE = (VALORANT_ROOT_FOLDER / 'live' / 'VALORANT.exe').resolve()
VALORANT_PAKS_FOLDER = (VALORANT_ROOT_FOLDER / 'live' / 'ShooterGame' / 'Content' / 'Paks').resolve()

SCRIPT_FOLDER = Path(os.path.join(os.getenv('LOCALAPPDATA'), 'VALTEXT')).resolve()

ENGLISH_FOLDER = (SCRIPT_FOLDER / 'English').resolve()
JAPANESE_FOLDER = (SCRIPT_FOLDER / 'Japanese').resolve()
SPANISH_FOLDER = (SCRIPT_FOLDER / 'Spanish').resolve()
FRENCH_FOLDER = (SCRIPT_FOLDER / 'French').resolve()
GERMAN_FOLDER = (SCRIPT_FOLDER / 'German').resolve()
ITALIAN_FOLDER = (SCRIPT_FOLDER / 'Italian').resolve()
PORTUGUESE_FOLDER = (SCRIPT_FOLDER / 'Portuguese').resolve()
RUSSIAN_FOLDER = (SCRIPT_FOLDER / 'Russian').resolve()
KOREAN_FOLDER = (SCRIPT_FOLDER / 'Korean').resolve()
CHINESE_FOLDER = (SCRIPT_FOLDER / 'Chinese').resolve()

languages = ['English', 'Japanese', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Russian', 'Korean',
             'Chinese']

ENGLISH_LANG_CODE = 'en_US_Text-WindowsClient'
JAPANESE_LANG_CODE = 'ja_JP_Text-WindowsClient'
SPANISH_LANG_CODE = 'es_ES_Text-WindowsClient'
FRENCH_LANG_CODE = 'fr_FR_Text-WindowsClient'
GERMAN_LANG_CODE = 'de_DE_Text-WindowsClient'
ITALIAN_LANG_CODE = 'it_IT_Text-WindowsClient'
PORTUGUESE_LANG_CODE = 'pt_BR_Text-WindowsClient'
RUSSIAN_LANG_CODE = 'ru_RU_Text-WindowsClient'
KOREAN_LANG_CODE = 'ko_KR_Text-WindowsClient'
CHINESE_LANG_CODE = 'zh_CN_Text-WindowsClient'

# Main Language Variables
TEXT_LANG_CODE = ENGLISH_LANG_CODE
TEXT_FOLDER = ENGLISH_FOLDER
VOICE_LANG_CODE = JAPANESE_LANG_CODE
VOICE_FOLDER = JAPANESE_FOLDER

default_text_language = 'English'
default_voice_language = 'Japanese'

LOG_FILE_FOLDER = Path(
    os.path.join(os.getenv('LOCALAPPDATA'), 'Riot Games', 'Riot Client', 'logs', 'riot client logs')).resolve()

# Color codes for print statements
COLOR_RESET = '\033[0m'
COLOR_GREEN = '\033[1;92m'
COLOR_YELLOW = '\033[1;93m'
COLOR_RED = '\033[1;91m'
COLOR_CYAN = '\033[1;96m'
COLOR_BOLD = '\033[1m'


def colored_print(message, color_code):
    return f"{color_code}{message}{COLOR_RESET}"


def debug_print(message):
    if debug_mode:
        print(colored_print(f"DEBUG: {message}", COLOR_RED))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored_print('----------------------------------', COLOR_GREEN))
    print(colored_print(f'ValText - Global Version {script_version}', COLOR_GREEN))
    print(colored_print('----------------------------------', COLOR_GREEN))


def display_welcome_message():
    if welcome_displayed:
        print(colored_print('Welcome', COLOR_GREEN))
        start_script = int(input(colored_print("Press '0' to Start, Any Other (1-9) for Misc: ", COLOR_YELLOW)))
        clear_screen()
        return start_script == 0


def create_required_folders():
    try:
        for folder in [SCRIPT_FOLDER, TEXT_FOLDER, VOICE_FOLDER]:
            folder.mkdir(parents=True, exist_ok=True)

        for filename in [f'{TEXT_LANG_CODE}.pak', f'{TEXT_LANG_CODE}.sig']:
            english_files = TEXT_FOLDER / filename
            if not english_files.exists():
                return False

        for filename in [f'{VOICE_LANG_CODE}.pak', f'{VOICE_LANG_CODE}.sig']:
            japanese_files = VOICE_FOLDER / filename
            if not japanese_files.exists():
                return False

        return True

    except Exception as error:
        print(colored_print(f"Error creating folders: {error}", COLOR_RED))
        return False


def copy_language_files(source_folder: Path, destination_folder: Path, filename: str):
    source_path = source_folder / filename
    destination_path = destination_folder / filename
    shutil.copy(source_path, destination_path)


def copy_english_language_files():
    global update_available, updating_game, update_completed, game_updated

    try:
        print(colored_print("Update complete. Changing language...", COLOR_GREEN))

        for filename in TEXT_FOLDER.iterdir():
            if filename.name.startswith('en_US'):
                new_filename = filename.name.replace('en_US', 'ja_JP')
                renamed_destination = VALORANT_PAKS_FOLDER / new_filename

                shutil.copy(filename, renamed_destination)

        print(colored_print("Language change successful.", COLOR_GREEN))
        return True

    except Exception as error:
        print(colored_print(f"An error occurred: {error}", COLOR_RED))
        return False


def start_valorant_game():
    valorant_path = str(RIOT_CLIENT_EXE)
    arguments = [
        '--launch-product=valorant',
        '--launch-patchline=live'
    ]

    try:
        subprocess.Popen([valorant_path] + arguments)
        print(colored_print("Launching Valorant through Riot Client Services...", COLOR_GREEN))
    except Exception as error:
        print(colored_print(f"Error launching Valorant: {error}", COLOR_RED))


def main_script():
    clear_screen()
    if display_welcome_message():
        print(colored_print('Checking for Files...', COLOR_YELLOW))
        if create_required_folders():
            if copy_japanese_language_files():
                if start_riot_client():
                    sleep(5)
                    log_file = find_latest_log_file()
                    if log_file:
                        debug_print(f"Found latest log file: '{log_file}'")
                        parse_log_file(log_file)
                    else:
                        handle_error()
                else:
                    handle_error()
            else:
                handle_error()
        else:
            handle_error()
    else:
        handle_error()


def copy_japanese_language_files():
    for filename in VOICE_FOLDER.iterdir():
        try:
            copy_language_files(VOICE_FOLDER, VALORANT_PAKS_FOLDER, filename.name)
        except Exception as error:
            debug_print(f"Error copying files: {error}")
            return False
    return True


def start_riot_client():
    riot_client_path = str(RIOT_CLIENT_EXE)

    debug_print(f"Checking Riot Client path: {riot_client_path}")

    if RIOT_CLIENT_EXE.exists():
        try:
            subprocess.Popen([riot_client_path])
            return True
        except Exception as error:
            debug_print(f"Error starting Riot Client: {error}")
            return False
    else:
        debug_print('Riot Client not found...')
        return False


def find_latest_log_file():
    log_files = glob.glob(os.path.join(LOG_FILE_FOLDER, '*.log'))
    if not log_files:
        return False

    log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return log_files[0]


def parse_log_file(log_file):
    global last_read_position

    while True:
        with open(log_file, 'r') as file:
            file.seek(last_read_position)

            log_files = glob.glob(os.path.join(LOG_FILE_FOLDER, '*.log'))
            log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

            latest_log = log_files[0]

            if log_file != latest_log:
                debug_print(f"Switching to read the new log file: {latest_log}")
                log_file = latest_log
                last_read_position = 0
                sleep(0.5)
                continue

            content = file.readlines()
            check_triggers(content)

            last_read_position = file.tell()


def check_triggers(log_lines):
    global update_available, updating_game, update_completed
    for line in log_lines:
        debug_print(f"Checking line: {line}")
        trigger_pattern = r'(\d+\.\d+)\|\s+ALWAYS\|\s+rnet-product-registry: TransitionToCombinedPatchState: install \'valorant.live\' switching states \'(.*?)\' -> \'(.*?)\' because \'statusPatchPlugin\''
        match = re.match(trigger_pattern, line)
        if match:
            debug_print(f"Trigger matched: \n{line}")
            old_state, new_state = match.group(2).strip('\''), match.group(3).strip('\'')
            if new_state == 'OutOfDate' and not update_available:
                update_available = True
                print(colored_print('Update available!', COLOR_YELLOW))
            if new_state == 'Updating' and not updating_game:
                updating_game = True
                print(colored_print('Updating Valorant! Please wait...', COLOR_YELLOW))
            if new_state == 'UpToDate' and not update_completed:
                update_completed = True
                print(colored_print('Valorant updated!', COLOR_GREEN))
                sleep(1)
                if copy_english_language_files():
                    start_valorant_game()
                    clear_screen()
                    print(colored_print("Closing in 7 Seconds!!", COLOR_GREEN))
                    sleep(5)
                    sys.exit()


def handle_error():
    clear_screen()
    question = input(colored_print("Do you want to Manually Set the Language Files (y/n): ", COLOR_YELLOW)).lower()
    if question == 'y' or question == 'yes':
        if change_language():
            if set_language_manually():
                main_script()
    else:
        print(colored_print("Contact Support Team", COLOR_RED))


def change_language():
    clear_screen()
    global TEXT_LANG_CODE, TEXT_FOLDER, VOICE_LANG_CODE, VOICE_FOLDER, default_text_language, default_voice_language

    print(colored_print('Current Languages:', COLOR_YELLOW))
    print(colored_print(f'Text Language: {default_text_language} - {TEXT_LANG_CODE}', COLOR_YELLOW))
    print(colored_print(f'Voice Language: {default_voice_language} - {VOICE_LANG_CODE}', COLOR_YELLOW))

    lang_input = input(colored_print('Do you want to change it? (yes/no): ', COLOR_YELLOW))

    if lang_input.lower() not in ['y', 'yes']:
        sys.exit()

    print(colored_print('Available Languages:', COLOR_YELLOW))
    for index, language in enumerate(languages, 1):
        print(colored_print(f'{index}. {language}', COLOR_YELLOW))
    print(colored_print('0. Exit', COLOR_YELLOW))

    def choose_language(language_type):
        input_message = f'Enter the number of the {language_type} Language: '
        language_input = int(input(colored_print(input_message, COLOR_YELLOW)))
        if language_input == 0:
            sys.exit()
        elif 1 <= language_input <= len(languages):
            return languages[language_input - 1]
        else:
            print(colored_print('Invalid input. Exiting...', COLOR_RED))
            sys.exit()

    default_text_language = choose_language('Text')
    default_voice_language = choose_language('Voice')

    language_mapping = {'English': ENGLISH_FOLDER, 'Japanese': JAPANESE_FOLDER, 'Spanish': SPANISH_FOLDER,
                        'French': FRENCH_FOLDER, 'German': GERMAN_FOLDER, 'Italian': ITALIAN_FOLDER,
                        'Portuguese': PORTUGUESE_FOLDER, 'Russian': RUSSIAN_FOLDER, 'Korean': KOREAN_FOLDER,
                        'Chinese': CHINESE_FOLDER}

    TEXT_FOLDER = language_mapping.get(default_text_language)
    TEXT_LANG_CODE = globals()[f"{default_text_language.upper()}_LANG_CODE"]

    VOICE_FOLDER = language_mapping.get(default_voice_language)
    VOICE_LANG_CODE = globals()[f"{default_voice_language.upper()}_LANG_CODE"]

    print(colored_print(f'Text Language: {default_text_language} - {TEXT_LANG_CODE}', COLOR_YELLOW))
    print(colored_print(f'Voice Language: {default_voice_language} - {VOICE_LANG_CODE}', COLOR_YELLOW))

    # Folders
    print(colored_print(f'Text Folder: {TEXT_FOLDER}', COLOR_YELLOW))
    print(colored_print(f'Voice Folder: {VOICE_FOLDER}', COLOR_YELLOW))

    return True


def set_language_manually():
    clear_screen()
    global TEXT_LANG_CODE, TEXT_FOLDER, VOICE_LANG_CODE, VOICE_FOLDER

    lang_manual = [default_text_language, default_voice_language]
    lang_codes = [TEXT_LANG_CODE, VOICE_LANG_CODE]
    folders = [TEXT_FOLDER, VOICE_FOLDER]

    for lang_manual, lang_code, folder in zip(lang_manual, lang_codes, folders):
        print(colored_print(f'Set to {lang_manual} - {lang_code}', '93'))
        input(colored_print('Press Enter to Continue...', '93'))

        source_pak = VALORANT_PAKS_FOLDER / f'{lang_code}.pak'
        destination_pak = folder / f'{lang_code}.pak'
        destination_pak.parent.mkdir(parents=True, exist_ok=True)

        source_sig = VALORANT_PAKS_FOLDER / f'{lang_code}.sig'
        destination_sig = folder / f'{lang_code}.sig'
        destination_sig.parent.mkdir(parents=True, exist_ok=True)

        try:
            clear_screen()
            print(colored_print(f"Copying {source_sig} to {destination_sig}\nCopying {source_pak} to {destination_pak}",
                                '92'))
            shutil.copy(source_sig, destination_sig)
            shutil.copy(source_pak, destination_pak)
            clear_screen()
            print(colored_print("Copy successful!", '92'))
            return True
        except FileNotFoundError as error:
            print(colored_print(f"Error copying {source_sig} to {destination_sig}: {error}", '31'))


# Execute the main_script function if the script is run as the main module
if __name__ == "__main__":
    main_script()
