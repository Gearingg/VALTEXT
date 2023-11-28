import os
import glob
import re
import shutil
import subprocess
import sys
import json
from pathlib import Path
from time import sleep

# Game Root Folder
RIOT_GAMES_ROOT_FOLDER = Path('D:/Riot Games').resolve()

# Game Executable
RIOT_CLIENT = (RIOT_GAMES_ROOT_FOLDER / 'Riot Client' / 'RiotClientServices.exe').resolve()

# VALORANT Content Folder
VALORANT_FILES = (RIOT_GAMES_ROOT_FOLDER / 'VALORANT' / 'live' / 'ShooterGame' / 'Content' / 'Paks').resolve()

# Supported Languages
SUPPORTED_LANGUAGES = {
    'English': 'en_US_Text-WindowsClient',
    'Japanese': 'ja_JP_Text-WindowsClient',
    'Spanish': 'es_ES_Text-WindowsClient',
    'French': 'fr_FR_Text-WindowsClient',
    'German': 'de_DE_Text-WindowsClient',
    'Italian': 'it_IT_Text-WindowsClient',
    'Portuguese': 'pt_BR_Text-WindowsClient',
    'Russian': 'ru_RU_Text-WindowsClient',
    'Korean': 'ko_KR_Text-WindowsClient',
    'Chinese': 'zh_CN_Text-WindowsClient'
}

# Script Folder
SCRIPT_FOLDER = Path(os.path.join(os.getenv('LOCALAPPDATA'), 'VALTEXT')).resolve()

DEFAULT_TEXT_LANGUAGE = 'English'
DEFAULT_TEXT_LANGUAGE_CODE = SUPPORTED_LANGUAGES[DEFAULT_TEXT_LANGUAGE]

# Default Text Language Folder
DEFAULT_TEXT_LANGUAGE_FOLDER = (SCRIPT_FOLDER / DEFAULT_TEXT_LANGUAGE).resolve()

# Default Text Language Files
DEFAULT_TEXT_LANGUAGE_PAK = (DEFAULT_TEXT_LANGUAGE_FOLDER / f'{DEFAULT_TEXT_LANGUAGE_CODE}.pak').resolve()
DEFAULT_TEXT_LANGUAGE_SIG = (DEFAULT_TEXT_LANGUAGE_FOLDER / f'{DEFAULT_TEXT_LANGUAGE_CODE}.sig').resolve()

# Default Voice Language Folder
DEFAULT_VOICE_LANGUAGE = 'Japanese'
DEFAULT_VOICE_LANGUAGE_CODE = SUPPORTED_LANGUAGES[DEFAULT_VOICE_LANGUAGE]

DEFAULT_VOICE_LANGUAGE_FOLDER = (SCRIPT_FOLDER / DEFAULT_VOICE_LANGUAGE).resolve()

# Default Voice Language Files
DEFAULT_VOICE_LANGUAGE_PAK = (DEFAULT_VOICE_LANGUAGE_FOLDER / f'{DEFAULT_VOICE_LANGUAGE_CODE}.pak').resolve()
DEFAULT_VOICE_LANGUAGE_SIG = (DEFAULT_VOICE_LANGUAGE_FOLDER / f'{DEFAULT_VOICE_LANGUAGE_CODE}.sig').resolve()

# Color codes for print statements
COLOR_RESET = '\033[0m'
COLOR_GREEN = '\033[1;92m'
COLOR_YELLOW = '\033[1;93m'
COLOR_RED = '\033[1;91m'
COLOR_CYAN = '\033[1;96m'
COLOR_BOLD = '\033[1m'
COLOR_PURPLE = '\033[1;95m'
COLOR_ORANGE = '\033[1;33m'
COLOR_GRAY = '\033[1;90m'


class Initialize:
    def __init__(self):
        print(Display().colored_screen('Initialization Started...', COLOR_ORANGE))
        sleep(2)
        pass

    @staticmethod
    def script_started():
        Display().clear_screen()
        if Display().welcome_screen():
            if Checks().create_folders():
                sleep(0.5)
                Display().clear_screen()
                if RiotGames().start_riot_client():
                    sleep(5)
                    Display().clear_screen()
                    LogFile().find_log()
                    LogFile().parse_log()
                else:
                    print(Display().debug_screen('Make sure you have the correct Riot Games Location in Config'))
            else:
                print(Display().debug_screen('Make sure you have permissions to make folders'))
        else:
            Settings()


class Display:
    def __init__(self):
        self.version = '0.1'
        self.branch = 'Test'
        self.debug = False

    @staticmethod
    def colored_screen(message, color_code):
        return f"{color_code}{message}{COLOR_RESET}"

    def debug_screen(self, message):
        if self.debug:
            print(self.colored_screen(f"DEBUG: {message}", COLOR_RED))

    def clear_screen(self=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.colored_screen('----------------------------------', COLOR_RED))
        print(self.colored_screen(f'ValText - {self.branch} Version {self.version}', COLOR_PURPLE))
        print(self.colored_screen('----------------------------------', COLOR_RED))
        return

    def welcome_screen(self):
        print(self.colored_screen('Welcome', COLOR_GREEN))
        start = int(input(self.colored_screen("Press 0 to Start, Any Other (1-9) for Settings: ", COLOR_GRAY)))
        if start == 0:
            self.clear_screen()
            return True
        elif start > 9:
            print(self.colored_screen("Omg, you're so Retarded", COLOR_RED))
            return False
        else:
            self.clear_screen()
            return False


class Checks:
    def __init__(self):
        self.text_pak_files = DEFAULT_TEXT_LANGUAGE_PAK
        self.text_sig_files = DEFAULT_TEXT_LANGUAGE_SIG
        self.voice_pak_files = DEFAULT_VOICE_LANGUAGE_PAK
        self.voice_sig_files = DEFAULT_VOICE_LANGUAGE_SIG

        self.text_code = DEFAULT_TEXT_LANGUAGE_CODE
        self.voice_code = DEFAULT_VOICE_LANGUAGE_CODE

        self.script_folder = SCRIPT_FOLDER
        self.text_folder = DEFAULT_TEXT_LANGUAGE_FOLDER
        self.voice_folder = DEFAULT_VOICE_LANGUAGE_FOLDER

        self.valorant_folder = VALORANT_FILES

    def create_folders(self):
        print(Display().colored_screen(f'Checking for Files...', COLOR_CYAN))
        try:
            for folder in [self.script_folder, self.text_folder, self.voice_folder]:
                folder.mkdir(parents=True, exist_ok=True)
            if not self.text_pak_files.exists() or not self.text_sig_files.exists() or \
                    not self.voice_pak_files.exists() or not self.voice_sig_files.exists():
                return False
            return True
        except Exception as error:
            print(Display().debug_screen(f"Error creating folders: {error}"))
            return False

    def copy_text_language_files(self):
        try:
            for filename in self.text_folder.iterdir():
                if filename.name.startswith(self.text_code):
                    print(Display().colored_screen(f'Copying Files...', COLOR_CYAN))
                    renamed_file = filename.name.replace(self.text_code, self.voice_code)
                    renameddestination = self.valorant_folder / renamed_file
                    shutil.copy(filename, renameddestination)

            print(Display().colored_screen(f'Copied all Files...', COLOR_GREEN))
            sleep(1)
            return True

        except Exception as error:
            print(Display().debug_screen(f"Error Copying Files: {error}"))
            return False

    def copy_voice_language_files(self):
        try:
            for filename in self.voice_folder.iterdir():
                if filename.name.startswith(self.voice_code):
                    shutil.copy(filename, self.valorant_folder)
                    return True
        except Exception as error:
            print(Display().debug_screen(f"Error Copying Files: {error}"))
            return False


class RiotGames:
    def __init__(self):
        self.riot_client = str(RIOT_CLIENT)

    def start_riot_client(self):
        try:
            subprocess.Popen([self.riot_client])
            print(Display().colored_screen(f"Starting Riot Client...", COLOR_CYAN))
            return True
        except Exception as error:
            print(Display().debug_screen(f"Error Starting Riot Client: {error}"))
            return False

    def start_valorant(self):
        arguments = [
            '--launch-product=valorant',
            '--launch-patchline=live'
        ]

        try:
            subprocess.Popen([self.riot_client] + arguments)
            print(Display().colored_screen(f"Launching Valorant...", COLOR_CYAN))
            return True
        except Exception as error:
            print(Display().debug_screen(f"Error Launching Valorant: {error}"))
            return False


class LogFile:
    def __init__(self):
        self.riot_base_path = Path(os.path.join(os.getenv('LOCALAPPDATA'), 'Riot Games')).resolve()
        self.client_logs_path = (self.riot_base_path / 'Riot Client' / 'logs ' / 'riot client logs').resolve()
        self.logfile = (self.riot_base_path / self.client_logs_path).resolve()
        self.last_read_position = 0

        self.log = None  # Initialize log with None
        self.new_log = None  # Initialize new_log with None

    def find_log(self):
        log_files = glob.glob(os.path.join(self.logfile, '*.log'))
        if not log_files:
            pass

        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        return log_files[0]

    def parse_log(self):
        while True:
            if self.log is None:
                self.log = self.find_log()  # If log is None, find the latest log file

            if not os.path.exists(self.log):
                print('Log file does not exist. Waiting for log file to be created...')
                sleep(1)
                continue

            with open(self.log, 'r') as file:
                file.seek(self.last_read_position)

                content = file.readlines()
                Triggers().check_triggers(content)

                self.last_read_position = file.tell()


class Triggers:
    def __init__(self):
        self.trigger_pattern = r'(\d+\.\d+)\|\s+ALWAYS\|\s+rnet-product-registry: TransitionToCombinedPatchState: install \'valorant.live\' switching states \'(.*?)\' -> \'(.*?)\' because \'statusPatchPlugin\''
        self.CurrentState = ''

    def check_triggers(self, log):
        for line in log:
            Display().debug_screen(f"Checking line: {line}")
            match = re.match(self.trigger_pattern, line)
            if match:
                Display().debug_screen(f"Trigger matched: \n{line}")
                old_state, new_state = match.group(2).strip('\''), match.group(3).strip('\'')
                if new_state == 'OutOfDate' and not self.CurrentState == 'OutofDate':
                    self.out_of_date()
                if new_state == 'Updating' and not self.CurrentState == 'Updating':
                    self.updating()
                if new_state == 'UpToDate' and not self.CurrentState == 'UpToDate':
                    self.updated()

    def out_of_date(self):
        if not self.CurrentState == 'OutofDate':
            self.CurrentState = 'OutofDate'
            print(Display().colored_screen('Update available!', COLOR_YELLOW))

    def updating(self):
        if not self.CurrentState == 'Updating':
            self.CurrentState = 'Updating'
            print(Display().colored_screen('Updating Valorant! Please wait...', COLOR_CYAN))

    def updated(self):
        if not self.CurrentState == 'UpToDate':
            self.CurrentState = 'UpToDate'
            print(Display().colored_screen('Valorant updated!', COLOR_GREEN))

            if Checks().copy_text_language_files():
                sleep(1)
                Display().clear_screen()
                if RiotGames().start_valorant():
                    print(Display().colored_screen('Valorant Launched', COLOR_GREEN))
                    Error().exit(5)


class Settings:
    def __init__(self):
        self.text_language = DEFAULT_TEXT_LANGUAGE
        self.text_language_code = DEFAULT_TEXT_LANGUAGE_CODE
        self.text_language_pak = DEFAULT_TEXT_LANGUAGE_PAK
        self.text_language_sig = DEFAULT_TEXT_LANGUAGE_SIG
        self.text_language_folder = DEFAULT_TEXT_LANGUAGE_FOLDER

        self.voice_language = DEFAULT_VOICE_LANGUAGE
        self.voice_language_code = DEFAULT_VOICE_LANGUAGE_CODE
        self.voice_language_pak = DEFAULT_TEXT_LANGUAGE_PAK
        self.voice_language_sig = DEFAULT_TEXT_LANGUAGE_SIG
        self.voice_language_folder = DEFAULT_TEXT_LANGUAGE_FOLDER

        self.text_input = 0
        self.voice_input = 0

        self.menu()

    def menu(self):
        print(Display().colored_screen(f'Do you want to\n1.Change Default Language\n2.Update Files', COLOR_ORANGE))
        answer = input(Display().colored_screen('Enter your Choice: ', COLOR_GRAY))
        if answer == '1':
            self.change_text_language()
            self.change_voice_language()
        elif answer == '2':
            self.set_language_manually()
        else:
            print(Display.colored_screen('No Such Option...', COLOR_RED))

    def change_language(self, language_type, default_language, default_language_code):
        global DEFAULT_TEXT_LANGUAGE, DEFAULT_VOICE_LANGUAGE
        print(Display().colored_screen(
            f'Current {language_type} Language: {default_language} | File Name: {default_language_code}', COLOR_YELLOW))

        change_lang_input = input("Do you want to change this language? (y/n): ").lower()

        if change_lang_input in ('y', 'yes'):
            print(Display().colored_screen(f'Supported Languages for {language_type}: ', COLOR_GREEN))
            for index, (language, code) in enumerate(SUPPORTED_LANGUAGES.items(), start=1):
                print(f"{index}. {language} ({code})")

            try:
                selected_index = int(input(f"Enter the number for the new {language_type} language: "))
                if 1 <= selected_index <= len(SUPPORTED_LANGUAGES):
                    selected_language, selected_language_code = list(SUPPORTED_LANGUAGES.items())[selected_index - 1]

                    setattr(self, f'{language_type.lower()}_language', selected_language)
                    setattr(self, f'{language_type.lower()}_language_code', selected_language_code)

                    if language_type == 'Text':
                        DEFAULT_TEXT_LANGUAGE = selected_language
                    elif language_type == 'Voice':
                        DEFAULT_VOICE_LANGUAGE = selected_language

                    Config().save_config()

                    Display().clear_screen()

                    return selected_language, selected_language_code  # Return the selected language

                else:
                    print(Display().colored_screen('Invalid input. No changes made.', COLOR_RED))
            except ValueError:
                print(Display().debug_screen('Invalid input. Please enter a valid number.'))
        elif change_lang_input in ('n', 'no'):
            pass
        else:
            print(Display().colored_screen('Invalid input. No changes made.', COLOR_RED))

        Display().clear_screen()

        return default_language, default_language_code  # Return the default language if no change is made

    def change_text_language(self):
        try:
            new_text_language, new_text_language_code = self.change_language('Text', self.text_language,
                                                                             self.text_language_code)
            print(Display().colored_screen(
                f'Text language changed to {new_text_language} ({new_text_language_code})',
                COLOR_GREEN))
        except Exception or WindowsError as er:
            print(Display().debug_screen(f"Error in change_text_language: {er}."))
            raise e

    def change_voice_language(self):
        try:
            new_voice_language, new_voice_language_code = self.change_language('Voice', self.voice_language,
                                                                               self.voice_language_code)
            print(Display().colored_screen(
                f'Voice language changed to {new_voice_language} ({new_voice_language_code})',
                COLOR_GREEN))
        except Exception or WindowsError as er:
            print(Display().debug_screen(f"Error in changing voice language: {er}."))
            raise e

    def set_language_manually(self):
        lang_manual = [self.text_language, self.voice_language]
        lang_codes = [self.text_language_code, self.voice_language_code]
        folders = [self.text_language_folder, self.voice_language_folder]

        for lang_manual, lang_code, folder in zip(lang_manual, lang_codes, folders):

            source_sig = VALORANT_FILES / f'{lang_code}.sig'
            source_pak = VALORANT_FILES / f'{lang_code}.pak'

            destination_sig = folder / f'{lang_code}.sig'
            destination_pak = folder / f'{lang_code}.pak'

            print(Display().colored_screen(f'Set to {lang_manual} - {lang_code}', COLOR_YELLOW))
            input(Display().colored_screen('Press Enter to Continue...', COLOR_YELLOW))

            try:
                print(Display().debug_screen(
                    f"Copying {source_sig} to {destination_sig}\nCopying {source_pak} to {destination_pak}"))
                shutil.copy(source_sig, destination_sig)
                shutil.copy(source_pak, destination_pak)
                print(Display().colored_screen("Copy successful!", COLOR_GREEN))
                return True
            except FileNotFoundError as error:
                print(Display().debug_screen(f"Error copying {source_sig} to {destination_sig}: {error}"))
                return False


class Error:
    def __init__(self):
        self.seconds = 0

    def exit(self, seconds):
        self.seconds = seconds
        sys.exit(self.seconds)


class Config:
    def __init__(self, filename='config.json'):
        self.filename = filename
        self.config = self.load_config()

    def save_config(self):
        script_folder = SCRIPT_FOLDER
        config_path = script_folder / self.filename

        with open(config_path, 'w') as file:
            json.dump({
                'RIOT_GAMES_ROOT_FOLDER': str(RIOT_GAMES_ROOT_FOLDER),
                'DEFAULT_TEXT_LANGUAGE': DEFAULT_TEXT_LANGUAGE,
                'DEFAULT_VOICE_LANGUAGE': DEFAULT_VOICE_LANGUAGE
            }, file)

    def load_config(self):
        script_folder = SCRIPT_FOLDER
        config_path = script_folder / self.filename

        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            return {
                'RIOT_GAMES_ROOT_FOLDER': config.get('RIOT_GAMES_ROOT_FOLDER', None),
                'DEFAULT_TEXT_LANGUAGE': config.get('DEFAULT_TEXT_LANGUAGE', None),
                'DEFAULT_VOICE_LANGUAGE': config.get('DEFAULT_VOICE_LANGUAGE', None)
            }
        except FileNotFoundError:
            return None

    def get_location(self):
        global default_text_language, default_voice_language
        global RIOT_GAMES_ROOT_FOLDER, DEFAULT_TEXT_LANGUAGE, DEFAULT_VOICE_LANGUAGE

        if not self.config:
            print(Display().colored_screen("Enter your Riot Games Folder Location:", COLOR_YELLOW))
            print(Display().colored_screen("Example: D:\\Riot Games", COLOR_CYAN))
            print(Display().colored_screen("Make sure it has both Riot Client and VALORANT Folders in it!!", COLOR_RED))
            answer = input(Display().colored_screen('Enter Location: ', COLOR_GRAY))

            default_text_language = input(Display().colored_screen(
                f"Enter the default text language\n ({', '.join(SUPPORTED_LANGUAGES.keys())}): ",
                COLOR_GRAY)).strip().title()

            default_voice_language = input(Display().colored_screen(
                f"Enter the default voice language (Current one in Riot Client )\n ({', '.join(SUPPORTED_LANGUAGES.keys())}): ",
                COLOR_GRAY)).strip().title()

            self.config = {
                'RIOT_GAMES_ROOT_FOLDER': answer,
                'DEFAULT_TEXT_LANGUAGE': default_text_language,
                'DEFAULT_VOICE_LANGUAGE': default_voice_language
            }

            self.save_config()

        return (
            Path(self.config['RIOT_GAMES_ROOT_FOLDER']).resolve(),
            self.config['DEFAULT_TEXT_LANGUAGE'],
            self.config['DEFAULT_VOICE_LANGUAGE']
        )


if __name__ == "__main__":
    try:
        riot_games_folder, default_text_language, default_voice_language = Config().get_location()
        RIOT_GAMES_ROOT_FOLDER = riot_games_folder
        DEFAULT_TEXT_LANGUAGE = default_text_language
        DEFAULT_VOICE_LANGUAGE = default_voice_language
        Initialize().script_started()
    except Exception as e:
        print(f"Error in main block: {e}")
        raise e
