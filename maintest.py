"""
Basic script to change the language of Valorant.
"""
import os
from pathlib import Path


class Display:
    """
    Display class to handle all display related functions.
    """
    def __init__(self, branch, version):
        self.version = version
        self.branch = branch

    def clear(self):
        """
        Clears the screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print('----------------------------------')
        print(f'ValText - {self.branch} Version {self.version}')
        print('----------------------------------')

    @staticmethod
    def debug(message):
        """
        Prints a debug message.
        """
        print(f'[DEBUG] {message}')


class Initialize:
    """
    Initialize class to handle all initialization related functions.
    """
    def __init__(self):
        # Default Language Settings
        self.default_text_language = 'English'
        if self.default_text_language == 'English':
            self.default_text_language_code = 'en_US'
            self.default_text_language_folder_name = 'English'

        self.default_voice_language = 'Japanese'
        if self.default_voice_language == 'Japanese':
            self.default_voice_language_code = 'ja_JP'
            self.default_voice_language_folder_name = 'Japanese'

        # Check if the language codes are not None before concatenating
        if self.default_text_language_code is not None:
            self.default_text_filename_pak = self.default_text_language_code + '_Text-WindowsClient' + '.pak'
            self.default_text_filename_sig = self.default_text_language_code + '_Text-WindowsClient' + '.sig'

        if self.default_voice_language_code is not None:
            self.default_voice_filename_pak = self.default_voice_language_code + '_VO-WindowsClient' + '.pak'
            self.default_voice_filename_sig = self.default_voice_language_code + '_VO-WindowsClient' + '.sig'

        self.default_script_folder = Path(os.path.join(os.getenv('LOCALAPPDATA'), 'VALTEXT')).resolve()

        self.default_text_language_folder = self.default_script_folder / self.default_text_language_folder_name
        self.default_voice_language_folder = self.default_script_folder / self.default_voice_language_folder_name

        if not self.create_required_folders():
            print('Error creating required folders. Please try again.')
            return

    def create_required_folders(self):
        """
        Creates the required folders.
        """
        try:
            for folder in [self.default_script_folder, self.default_text_language_folder,
                           self.default_voice_language_folder]:
                folder.mkdir(parents=True, exist_ok=True)

            for filename in [self.default_text_filename_pak, self.default_text_filename_sig]:
                english_files = self.default_text_language_folder / filename
                if not english_files.exists():
                    return False

            for filename in [self.default_voice_filename_pak, self.default_voice_filename_sig]:
                japanese_files = self.default_voice_language_folder / filename
                if not japanese_files.exists():
                    return False

            return True

        except OSError as error:
            print(f"Error creating folders: {error}")
            return False

    def welcome(self):
        """
        Displays the welcome screen.
        """
        print('Welcome to ValText!')
        print('Please select an option below:')
        print('1. Start Script')
        print('9. Exit')
        print('Any other key for Settings')
        option = int(input('Enter an option: '))
        if option == '1':
            pass
        elif option == '9':
            pass
        else:
            self.settings()

    def settings(self):
        """
        Displays the settings screen.
        """
        display_instance.clear()
        print('Settings')
        print('Please select an option below:')
        print('1. Change Language')
        print('2. Fix Language Files')
        print('Any other key for Main Menu')
        option = input('Enter an option: ')
        if option == '1':
            pass
        elif option == '2':
            pass
        else:
            self.welcome()


class Files:
    """
    Files class to handle all file related functions.
    """
    def __init__(self):
        # Default Language Settings
        self.default_text_language = 'English'
        if self.default_text_language == 'English':
            self.default_text_language_code = 'en_US'
            self.default_text_language_folder_name = 'English'

        self.default_voice_language = 'Japanese'
        if self.default_voice_language == 'Japanese':
            self.default_voice_language_code = 'ja_JP'
            self.default_voice_language_folder_name = 'Japanese'

        self.default_text_filename_pak = self.default_text_language_code + '_Text-WindowsClient' + '.pak'
        self.default_text_filename_sig = self.default_text_language_code + '_Text-WindowsClient' + '.sig'

        self.default_voice_filename_pak = self.default_voice_language_code + '_VO-WindowsClient' + '.pak'
        self.default_voice_filename_sig = self.default_voice_language_code + '_VO-WindowsClient' + '.sig'

        self.default_script_folder = Path(os.path.join(os.getenv('LOCALAPPDATA'), 'VALTEXT')).resolve()

        self.default_text_language_folder_pak = self.default_script_folder / self.default_text_language_folder_name / self.default_text_filename_pak
        self.default_text_language_folder_sig = self.default_script_folder / self.default_text_language_folder_name / self.default_text_filename_sig
        self.default_voice_language_folder_pak = self.default_script_folder / self.default_voice_language_folder_name / self.default_voice_filename_pak
        self.default_voice_language_folder_sig = self.default_script_folder / self.default_voice_language_folder_name / self.default_voice_filename_sig

    def copy_files(self):
        """
        Copies the files.
        """
display_instance = Display(branch='Global', version='1.0.0')
initialize_instance = Initialize()


if __name__ == '__main__':
    pass
