# external
# python native
import logging,os,configparser,pathlib
# project

class Config:
    '''
    WARINING: Project specific changes are to be made in the marked area (CUSTOM SECTION below).
    The following things are handled by this class:
    - Generation of required folders
    - Generation of config.ini
    - Checking if config.ini is damaged and regeneration or adding missing parameters
    - writing and reading from config.ini
    '''
    # class variables
    folders = {}
    INI_FILE: pathlib.Path()
    DB_FILE: pathlib.Path()
    config: configparser.ConfigParser()
    _instance = None
    
    def __new__(cls):
        # Turns this class into a singleton
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance


    def __init__(self):
        '''Init, but only executed once'''
        if not self._initialized:
            self.folders["root"] = pathlib.Path(__file__).parent.parent.parent
            self.config = configparser.ConfigParser()
            self.custom_files()
            self.ensureBaseFolders()
            self._initialized = True
    

    def generateConfig(self):
        '''Generates entire configuration anew, this will CLEAR any previous configuration'''
        self.config = self.custom_default_config()

        self.writeConfig()
        
        logging.info("Success! config.ini has been created!")
        logging.info("Change its parameters and restart the program.")
        exit()


    def checkConfig(self):
        '''Check if config.ini is present, and whether it's incomplete. Repairs missing parts.'''

        # Check if 'config.ini' is present
        if not os.path.exists(self.INI_FILE):
            logging.warning("ini file doesen't exist, creating...")
            self.generateConfig()

        # Check if 'config.ini' is missing sections or keys
        defaultconfig = self.custom_default_config()
        self.config.read(self.INI_FILE)

        # Adding missing sections/keys (Using defaultconfig as basefile)
        for section in defaultconfig.sections():
            # Adding sections
            if not section in self.config.sections():
                logging.warning(f"Section '{section}' missing. Adding it now.")
                self.config.add_section(section)
            
            # Adding keys to sections
            for defaultkey in defaultconfig.items(section):
                currentKeys = []

                # Create list of current section keys
                for key in self.config.items(section):
                    currentKeys.append(key[0])

                if not defaultkey[0] in currentKeys:
                    logging.warning(f"Key '{defaultkey[0]}' missing. Adding it now.")
                    self.config[section][defaultkey[0]] = defaultkey[1]
                
        self.writeConfig()
        logging.info("Config check completed.")


    def writeConfig(self):
        '''Write config to file'''
        try:
            with open(self.INI_FILE, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            logging.error(f"Failed to write 'config.ini': {e}")
            exit()

    def ensureBaseFolders(self):
        '''Creates all folders listed '''
        for folder in self.folders.values():
            self.ensureFolder(folder)


    @staticmethod
    def ensureFolder(folder_path: pathlib.Path):
        '''takes path, and creates missing folders in that path if they don't exist'''
        
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except Exception as e:
                logging.error(f"Failed to create directories for {folder_path}: {e}")

    #
    # ------ GETTER ------
    #

    def get_config(self, category, key):
        '''Calling just the string within the .ini without any checks'''
        
        try:
            return self.config[category][key]
        except Exception as e:
            logging.error(f"Failed to read 'config.ini': {e}")


    def get_datafolder(self) -> pathlib.Path:
        return self.DATA_FOLDER


    def get_inipath(self) -> pathlib.Path:
        return self.INI_FILE

    def get_dbpath(self) -> pathlib.Path:
        return self.DB_FILE


    def get_logpath(self) -> pathlib.Path:
        pass


    def get_loglevel(self) -> int:
        '''Returns integer value of string in the config. Defaults to info'''
        loglevel_input = self.get_config("SCRIPT","loglevel").lower()

        loglevels = {"debug": 10, "info": 20, "warning": 30, "error": 40, "critical": 50}
            
        if loglevel_input in loglevels:
            return loglevels[loglevel_input]
        
        logging.error("Failed to determine loglevel, defaulting to debug.")
        return 20


    def get_bot_prefix(self):
        '''Attempts to get bot prefix from config.ini. Defaults to "!".'''
        prefix = self.get_config("CLIENT","prefix")

        if prefix == "":
            logging.error("No Prefix configured, defaulted to '!'")
            prefix = "!"
        
        return prefix

    #
    # ------ SETTER ------
    #

    def set_config(self, category, key, value):
        ''''Sets config option.'''
        self.config[category][key] = value
        self.writeConfig()

    ########################
    # CUSTOM SECTION
    ########################

    def custom_files(self):
        '''This is where you can add custom locations that should be handled by the class.'''
        self.folders["data"] = os.path.join(self.folders["root"], "data")
        #self.folders["sounds"] = os.path.join(self.folders["data"], "sounds")
        #self.folders["sounds_default"] = os.path.join(self.folders["sounds"], "default") # Hardcoded folders, cannot be played with /play command
        #self.folders["sounds_custom"] = os.path.join(self.folders["sounds"], "custom")
        self.INI_FILE = os.path.join(self.folders["data"], "config.ini")
        self.DB_FILE = os.path.join(self.folders["data"], "database.db")

        
    def custom_default_config(self):
        '''Here you can define the .ini file you want generated'''
        defaultconfig = configparser.ConfigParser()

        defaultconfig['AUTH'] = {
            "client_id" : "",
            "client_secret" : ""
        }

        defaultconfig['SCRIPT'] = {
            "loglevel" : "info"
        }

        return defaultconfig