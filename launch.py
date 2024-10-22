import os
import json
import subprocess
import random
import re

CONFIG_GENERATED = "/reforger/Configs/docker_generated.json"

def env_defined(key):
    return key in os.environ and len(os.environ[key]) > 0

def bool_str(text):
    return text.lower() == "true"

def random_passphrase():
    r_password = "'"
    while "'" in r_password:
        with open("/usr/share/dict/american-english") as f:
            words = f.readlines()
        r_password = "-".join(random.sample(words, 2)).replace("\n", "").lower()
    return r_password

def steamcmd_install():
    """
    Executes SteamCMD to install or update the game server.
    """
    steamcmd = ["/steamcmd/steamcmd.sh"]
    steamcmd.extend(["+force_install_dir", "/reforger"])
    if env_defined("STEAM_USER"):
        steamcmd.extend(
            ["+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"]]
        )
    else:
        steamcmd.extend(["+login", "anonymous"])
    steamcmd.extend(["+app_update", os.environ["STEAM_APPID"]])
    if env_defined("STEAM_BRANCH"):
        steamcmd.extend(["-beta", os.environ["STEAM_BRANCH"]])
    if env_defined("STEAM_BRANCH_PASSWORD"):
        steamcmd.extend(["-betapassword", os.environ["STEAM_BRANCH_PASSWORD"]])
    steamcmd.extend(["validate", "+quit"])
    
    print(f"Running SteamCMD: {' '.join(steamcmd)}")
    subprocess.call(steamcmd)

def get_secret_or_env_value(env_var_name):
    """
    Fetches the value of an environment variable. If the value starts with '/run/secrets/',
    it reads the content of the file at that location (Docker secret). Otherwise, it returns the variable value directly.
    
    :param env_var_name: Name of the environment variable to check.
    :return: The value from the secret file or the environment variable value.
    """
    value = None
    if env_defined(env_var_name):
        value = os.environ[env_var_name]
        
        if value.startswith('/run/secrets/'):
            try:
                with open(value, 'r') as secret_file:
                    secret_value = secret_file.read().strip()
                    print(f"{env_var_name}: '{secret_value}'")
                    value = secret_value
            except FileNotFoundError:
                print(f"Secret file '{value}' not found for {env_var_name}.")
            except Exception as e:
                print(f"Error reading secret file for {env_var_name}: '{e}'")
    return value

# Ensure the gameProperties dictionary is initialized.
def ensure_game_properties(config):
    if "gameProperties" not in config["game"]:
        config["game"]["gameProperties"] = {}

def generate_config():
    """
    Generates the game server configuration based on environment variables.
    Loads, modifies, and saves the configuration file.
    """
    if os.environ["ARMA_CONFIG"] != "docker_generated":
        config_path = f"/reforger/Configs/{os.environ['ARMA_CONFIG']}"
    else:
        # Load the default or generated config
        if os.path.exists(CONFIG_GENERATED):
            with open(CONFIG_GENERATED) as f:
                config = json.load(f)
        else:
            with open("/docker_default.json") as f:
                config = json.load(f)
                
        # Modify the config based on environment variables
        if env_defined("SERVER_BIND_ADDRESS"):
            config["bindAddress"] = os.environ["SERVER_BIND_ADDRESS"]
        if env_defined("SERVER_BIND_PORT"):
            config["bindPort"] = int(os.environ["SERVER_BIND_PORT"])
        if env_defined("SERVER_PUBLIC_ADDRESS"):
            config["publicAddress"] = os.environ["SERVER_PUBLIC_ADDRESS"]
        if env_defined("SERVER_PUBLIC_PORT"):
            config["publicPort"] = int(os.environ["SERVER_PUBLIC_PORT"])
        if env_defined("SERVER_A2S_ADDRESS") and env_defined("SERVER_A2S_PORT"):
            config["a2s"] = {
                "address": os.environ["SERVER_A2S_ADDRESS"],
                "port": int(os.environ["SERVER_A2S_PORT"]),
            }
        else:
            config["a2s"] = None

        if env_defined("RCON_ADDRESS") and env_defined("RCON_PORT"):
            config["rcon"] = {
                "address": os.environ["RCON_ADDRESS"],
                "port": int(os.environ["RCON_PORT"]),
                "password": os.environ["RCON_PASSWORD"],
                "permission": os.environ["RCON_PERMISSION"],
            }
        else:
            config["rcon"] = None

        # Game settings
        if env_defined("GAME_NAME"):
            config["game"]["name"] = os.environ["GAME_NAME"]

        if env_defined("GAME_PASSWORD"):
            config["game"]["password"] = get_secret_or_env_value("GAME_PASSWORD")

        if env_defined("GAME_PASSWORD_ADMIN"):
            config["game"]["passwordAdmin"] = get_secret_or_env_value("GAME_PASSWORD_ADMIN")
        else:
            admin_password = random_passphrase()
            config["game"]["passwordAdmin"] = admin_password
            print(f"Admin password: {admin_password}")
            
        # Admins and other game properties
        if env_defined("GAME_ADMINS"):
            admins = str(os.environ["GAME_ADMINS"]).split(",")
            admins[:] = [admin for admin in admins if admin]  # Remove empty items
            config["game"]["admins"] = admins
        if env_defined("GAME_SCENARIO_ID"):
            config["game"]["scenarioId"] = os.environ["GAME_SCENARIO_ID"]
        if env_defined("GAME_MAX_PLAYERS"):
            config["game"]["maxPlayers"] = int(os.environ["GAME_MAX_PLAYERS"])
        if env_defined("GAME_VISIBLE"):
            config["game"]["visible"] = bool_str(os.environ["GAME_VISIBLE"])
        if env_defined("GAME_SUPPORTED_PLATFORMS"):
            config["game"]["supportedPlatforms"] = os.environ["GAME_SUPPORTED_PLATFORMS"].split(",")
        
        # When running test check out comment next line 
        # to ensure gameProperties is set
        ensure_game_properties(config)
        if env_defined("GAME_PROPS_BATTLEYE"):
            config["game"]["gameProperties"]["battlEye"] = bool_str(os.environ["GAME_PROPS_BATTLEYE"])
        if env_defined("GAME_PROPS_DISABLE_THIRD_PERSON"):
            config["game"]["gameProperties"]["disableThirdPerson"] = bool_str(os.environ["GAME_PROPS_DISABLE_THIRD_PERSON"])
        if env_defined("GAME_PROPS_FAST_VALIDATION"):
            config["game"]["gameProperties"]["fastValidation"] = bool_str(os.environ["GAME_PROPS_FAST_VALIDATION"])
        if env_defined("GAME_PROPS_SERVER_MAX_VIEW_DISTANCE"):
            config["game"]["gameProperties"]["serverMaxViewDistance"] = int(os.environ["GAME_PROPS_SERVER_MAX_VIEW_DISTANCE"])
        if env_defined("GAME_PROPS_SERVER_MIN_GRASS_DISTANCE"):
            config["game"]["gameProperties"]["serverMinGrassDistance"] = int(os.environ["GAME_PROPS_SERVER_MIN_GRASS_DISTANCE"])
        if env_defined("GAME_PROPS_NETWORK_VIEW_DISTANCE"):
            config["game"]["gameProperties"]["networkViewDistance"] = int(os.environ["GAME_PROPS_NETWORK_VIEW_DISTANCE"])

        # Mod configurations
        config["game"]["mods"] = []
        config_mod_ids = []
        if env_defined("GAME_MODS_IDS_LIST"):
            reg = re.compile(r"^[A-Z\d,=.]+$")
            assert reg.match(str(os.environ["GAME_MODS_IDS_LIST"])), "Illegal characters in GAME_MODS_IDS_LIST env"
            mods = str(os.environ["GAME_MODS_IDS_LIST"]).split(",")
            mods[:] = [mod for mod in mods if mod]
            reg = re.compile(r"^\d+\.\d+\.\d+$")
            for mod in mods:
                mod_details = mod.split("=")
                assert 0 < len(mod_details) < 3, f"{mod} mod not defined properly"
                mod_id = mod_details[0]
                if mod_id in config_mod_ids:
                    continue  # Skip duplicates
                mod_config = {"modId": mod_id}
                if len(mod_details) == 2:
                    assert reg.match(mod_details[1]), f"{mod} mod version does not match the pattern"
                    mod_config["version"] = mod_details[1]
                config_mod_ids.append(mod_id)
                config["game"]["mods"].append(mod_config)

        if env_defined("GAME_MODS_JSON_FILE_PATH"):
            with open(os.environ["GAME_MODS_JSON_FILE_PATH"]) as f:
                json_mods = json.load(f)
                allowed_keys = ["modId", "name", "version"]
                for provided_mod in json_mods:
                    assert "modId" in provided_mod, f"Entry in GAME_MODS_JSON_FILE_PATH file does not contain modId: {provided_mod}"
                    if provided_mod["modId"] in config_mod_ids:
                        continue  # Skip duplicates
                    valid_mod = {key: provided_mod[key] for key in allowed_keys if key in provided_mod}
                    config_mod_ids.append(provided_mod["modId"])
                    config["game"]["mods"].append(valid_mod)

        # Write the modified config to the generated config file
        with open(CONFIG_GENERATED, "w") as f:
            json.dump(config, f, indent=4)

        config_path = CONFIG_GENERATED

    return config_path

if __name__ == "__main__":
    # Call the SteamCMD installation function if SKIP_INSTALL is not set or false
    if os.environ.get("SKIP_INSTALL", "false").lower() != "true":
        steamcmd_install()

    # Generate the config file
    config_path = generate_config()

    # Build and execute the launch command
    launch_command = " ".join([
        os.environ["ARMA_BINARY"],
        f"-config {config_path}",
        "-backendlog",
        "-nothrow",
        f"-maxFPS {os.environ['ARMA_MAX_FPS']}",
        f"-profile {os.environ['ARMA_PROFILE']}",
        f"-addonDownloadDir {os.environ['ARMA_WORKSHOP_DIR']}",
        f"-addonsDir {os.environ['ARMA_WORKSHOP_DIR']}",
        os.environ["ARMA_PARAMS"],
    ])
    print(launch_command, flush=True)
    os.system(launch_command)
