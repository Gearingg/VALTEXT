import os
import glob
import re
import shutil
import subprocess
import sys
from pathlib import Path
from time import sleep

# Script Variables
script_version = '1.0'
debug_mode = False

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

# Log File Folder
LOG_FILE_FOLDER = Path(os.path.join(os.getenv('LOCALAPPDATA'), 'Riot Games', 'Riot Client', 'logs', 'riot client logs')).resolve()

# Script Folder
SCRIPT_FOLDER = Path(os.path.join(os.getenv('LOCALAPPDATA'), 'VALTEXT')).resolve()

DEFAULT_TEXT_LANGUAGE = 'English'
DEFAULT_TEXT_LANGUAGE_CODE = SUPPORTED_LANGUAGES[DEFAULT_TEXT_LANGUAGE]

# Default Text Language Folder
DEFAULT_TEXT_LANGUAGE_FOLDER = (SCRIPT_FOLDER / DEFAULT_TEXT_LANGUAGE).resolve()

# Default Text Language Files
DEFAULT_TEXT_LANGUAGE_PAK = (DEFAULT_TEXT_LANGUAGE_FOLDER / DEFAULT_TEXT_LANGUAGE_CODE / '.pak').resolve()
DEFAULT_TEXT_LANGUAGE_SIG = (DEFAULT_TEXT_LANGUAGE_FOLDER / DEFAULT_TEXT_LANGUAGE_CODE / '.sig').resolve()

# Default Voice Language Folder
DEFAULT_VOICE_LANGUAGE = 'Japanese'
DEFAULT_VOICE_LANGUAGE_CODE = SUPPORTED_LANGUAGES[DEFAULT_VOICE_LANGUAGE]

DEFAULT_VOICE_LANGUAGE_FOLDER = (SCRIPT_FOLDER / DEFAULT_VOICE_LANGUAGE).resolve()

# Default Voice Language Files
DEFAULT_VOICE_LANGUAGE_PAK = (DEFAULT_VOICE_LANGUAGE_FOLDER / DEFAULT_VOICE_LANGUAGE_CODE / '.pak').resolve()
DEFAULT_VOICE_LANGUAGE_SIG = (DEFAULT_VOICE_LANGUAGE_FOLDER / DEFAULT_VOICE_LANGUAGE_CODE / '.sig').resolve()

# Color codes for print statements
COLOR_RESET = '\033[0m'
COLOR_GREEN = '\033[1;92m'
COLOR_YELLOW = '\033[1;93m'
COLOR_RED = '\033[1;91m'
COLOR_CYAN = '\033[1;96m'
COLOR_BOLD = '\033[1m'


class Initialize:
    def __init__(self):
        pass

    @staticmethod
    def script_started():
        display.clear_screen()
        display.welcome_screen()
        checks.create_folders()
        checks.copy_voice_language_files()
        riotgames.start_riot_client()
        sleep(5)
        log_file.find_log()
        log_file.parse_log()


class Display:
    def __init__(self):
        self.version = script_version
        self.debug = debug_mode

    @staticmethod
    def colored_screen(message, color_code):
        return f"{color_code}{message}{COLOR_RESET}"

    def debug_screen(self, message):
        if self.debug:
            print(self.colored_screen(f"DEBUG: {message}", COLOR_RED))
            return True
        else:
            return False

    def clear_screen(self=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.colored_screen('----------------------------------', COLOR_RED))
        print(self.colored_screen(f'ValText - Global Version {self.version}', COLOR_GREEN))
        print(self.colored_screen('----------------------------------', COLOR_RED))
        return

    def welcome_screen(self):
        print(self.colored_screen('Welcome', COLOR_GREEN))
        start = int(input(self.colored_screen("Press 0 to Start, Any Other (1-9) for Settings: ", COLOR_YELLOW)))
        if start == 0:
            self.clear_screen()
            return True
        elif start > 9:
            print(self.colored_screen("Omg, you're so Retarded", COLOR_RED))
            return True
        else:
            self.clear_screen()
            return False


class Checks:
    def __init__(self):
        self.text_pak_files = DEFAULT_TEXT_LANGUAGE_FOLDER / f'{DEFAULT_TEXT_LANGUAGE_CODE}.pak'
        self.text_sig_files = DEFAULT_TEXT_LANGUAGE_FOLDER / f'{DEFAULT_TEXT_LANGUAGE_CODE}.sig'
        self.voice_pak_files = DEFAULT_VOICE_LANGUAGE_FOLDER / f'{DEFAULT_VOICE_LANGUAGE_CODE}.pak'
        self.voice_sig_files = DEFAULT_VOICE_LANGUAGE_FOLDER / f'{DEFAULT_VOICE_LANGUAGE_CODE}.sig'

    def create_folders(self):
        try:
            for folder in [SCRIPT_FOLDER, DEFAULT_TEXT_LANGUAGE_FOLDER, DEFAULT_VOICE_LANGUAGE_FOLDER]:
                folder.mkdir(parents=True, exist_ok=True)
            if not self.text_pak_files.exists() or not self.text_sig_files.exists() or \
                    not self.voice_pak_files.exists() or not self.voice_sig_files.exists():
                return False
            return True
        except Exception as error:
            print(Display.colored_screen(f"Error creating folders: {error}", COLOR_RED))
            return False

    def copy_text_language_files(self):
        try:
            shutil.copy(self.text_pak_files, VALORANT_FILES)
            shutil.copy(self.text_sig_files, VALORANT_FILES)
            return True
        except Exception as error:
            print(Display.colored_screen(f"Error Copying Files: {error}", COLOR_RED))
            print('Error in Text')
            return False

    def copy_voice_language_files(self):
        try:
            shutil.copy(self.voice_pak_files, VALORANT_FILES)
            shutil.copy(self.voice_sig_files, VALORANT_FILES)
            return True
        except Exception as error:
            print(Display.colored_screen(f"Error Copying Files: {error}", COLOR_RED))
            print('Error in voice')
            return False


class RiotGames:
    def __init__(self):
        self.riot_client = str(RIOT_CLIENT)

    def start_riot_client(self):
        try:
            subprocess.Popen([self.riot_client])
            print(Display.colored_screen(f"Starting Riot Client...", COLOR_CYAN))
            return True
        except Exception as error:
            print(Display.colored_screen(f"Error Starting Riot Client: {error}", COLOR_RED))
            return False

    def start_valorant(self):
        arguments = [
            '--launch-product=valorant',
            '--launch-patchline=live'
        ]

        try:
            subprocess.Popen([self.riot_client] + arguments)
            print(Display.colored_screen(f"Launching Valorant...", COLOR_CYAN))
            return True
        except Exception as error:
            print(Display.colored_screen(f"Error launching Valorant: {error}", COLOR_RED))
            return False


class LogFile:
    def __init__(self):
        self.last_read_position = 0
        self.log = LOG_FILE_FOLDER
        self.new_log = None

    def find_log(self):
        log_files = glob.glob(os.path.join(self.log, '*.log'))
        if not log_files:
            return False

        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        self.log = log_files[0]

        return True

    def parse_log(self):
        while True:
            with open(self.log, 'r') as file:
                file.seek(self.last_read_position)

                self.new_log = self.find_log()

                if self.log != self.new_log:
                    display.debug_screen(f"Switching to read the new log file: {self.new_log}")
                    self.log = self.new_log
                    self.last_read_position = 0
                    sleep(0.5)
                    continue

                content = file.readlines()
                triggers.check_triggers(content)

                self.last_read_position = file.tell()


class Triggers:
    def __init__(self):
        self.trigger_pattern = r'(\d+\.\d+)\|\s+ALWAYS\|\s+rnet-product-registry: TransitionToCombinedPatchState: install \'valorant.live\' switching states \'(.*?)\' -> \'(.*?)\' because \'statusPatchPlugin\''
        self.CurrentState = ''

    def check_triggers(self, log):
        for line in log:
            display.debug_screen(f"Checking line: {line}")
            match = re.match(self.trigger_pattern, line)
            if match:
                display.debug_screen(f"Trigger matched: \n{line}")
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
            print(Display.colored_screen('Update available!', COLOR_YELLOW))

    def updating(self):
        if not self.CurrentState == 'Updating':
            self.CurrentState = 'Updating'
            print(Display.colored_screen('Updating Valorant! Please wait...', COLOR_CYAN))

    def updated(self):
        if not self.CurrentState == 'UpToDate':
            self.CurrentState = 'UpToDate'
            print(Display.colored_screen('Valorant updated!', COLOR_GREEN))

            checks.copy_text_language_files()
            sleep(1)
            riotgames.start_valorant()
            errors.exit(5)


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

    def change_language(self, language_type, default_language, default_language_code):
        print(Display.colored_screen(f'Current {language_type} Language: {default_language} File Name: {default_language_code}', COLOR_YELLOW))

        change_lang_input = input("Do you want to change this language? (y/n): ").lower()

        if change_lang_input in ('y', 'yes'):
            print(Display.colored_screen(f'Supported Languages for {language_type}: ', COLOR_YELLOW))
            for index, (language, code) in enumerate(SUPPORTED_LANGUAGES.items(), start=1):
                print(f"{index}. {language} ({code})")

            try:
                selected_index = int(input(f"Enter the number for the new {language_type} language: "))
                if 1 <= selected_index <= len(SUPPORTED_LANGUAGES):
                    selected_language = list(SUPPORTED_LANGUAGES.keys())[selected_index - 1]
                    selected_language_code = list(SUPPORTED_LANGUAGES.values())[selected_index - 1]

                    setattr(self, f'{language_type.lower()}_language', selected_language)
                    setattr(self, f'{language_type.lower()}_language_code', selected_language_code)

                    print(Display.colored_screen(f'{language_type} language changed to {selected_language} ({selected_language_code})', COLOR_GREEN))

                    # Update default language variables
                    if language_type == 'Text':
                        global DEFAULT_TEXT_LANGUAGE, DEFAULT_TEXT_LANGUAGE_CODE
                        DEFAULT_TEXT_LANGUAGE, DEFAULT_TEXT_LANGUAGE_CODE = selected_language, selected_language_code
                    elif language_type == 'Voice':
                        global DEFAULT_VOICE_LANGUAGE, DEFAULT_VOICE_LANGUAGE_CODE
                        DEFAULT_VOICE_LANGUAGE, DEFAULT_VOICE_LANGUAGE_CODE = selected_language, selected_language_code

                else:
                    print(Display.colored_screen('Invalid input. No changes made.', COLOR_RED))
            except ValueError:
                print(Display.colored_screen('Invalid input. Please enter a valid number.', COLOR_RED))
        elif change_lang_input in ('n', 'no'):
            pass
        else:
            print(Display.colored_screen('Invalid input. No changes made.', COLOR_RED))

    def change_text_language(self):
        self.change_language('Text', self.text_language, self.text_language_code)

        print(self.text_language)
        print(self.text_language_code)
        print(self.text_language_folder)
        print(self.text_language_pak)
        print(self.text_language_sig)

    def change_voice_language(self):
        self.change_language('Voice', self.voice_language, self.voice_language_code)

    def set_language_manually(self):
        lang_manual = [self.text_language, self.voice_language]
        lang_codes = [self.text_language_code, self.voice_language_code]
        folders = [self.text_language_folder, self.voice_language_folder]

        for lang_manual, lang_code, folder in zip(lang_manual, lang_codes, folders):

            source_sig = VALORANT_FILES / f'{lang_code}.sig'
            source_pak = VALORANT_FILES / f'{lang_code}.pak'

            destination_sig = folder / f'{lang_code}.sig'
            destination_pak = folder / f'{lang_code}.pak'

            print(Display.colored_screen(f'Set to {lang_manual} - {lang_code}', COLOR_YELLOW))
            input(Display.colored_screen('Press Enter to Continue...', COLOR_YELLOW))

            try:
                print(Display.colored_screen(f"Copying {source_sig} to {destination_sig}\nCopying {source_pak} to {destination_pak}", COLOR_GREEN))
                shutil.copy(source_sig, destination_sig)
                shutil.copy(source_pak, destination_pak)
                print(Display.colored_screen("Copy successful!", COLOR_GREEN))
                return True
            except FileNotFoundError as error:
                print(Display.colored_screen(f"Error copying {source_sig} to {destination_sig}: {error}", COLOR_RED))
                return False


class Error:
    def __init__(self):
        self.seconds = 0

    def exit(self, seconds):
        self.seconds = seconds
        sys.exit(self.seconds)


if __name__ == "__main__":
    #initialize = Initialize()
    #display = Display()
    checks = Checks()
    #riotgames = RiotGames()
    #log_file = LogFile()
    #triggers = Triggers()
    #settings = Settings()
    #errors = Error()
    #initialize.script_started()

    checks.copy_text_language_files()
