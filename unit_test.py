import unittest
from unittest.mock import patch, mock_open, MagicMock
import os

#DEBUG ENV
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Unit test for get_secret_or_env_value function

class TestConfigScript(unittest.TestCase):

    @patch.dict(os.environ, {"GAME_PASSWORD": "/run/secrets/game_password"})
    @patch("builtins.open", new_callable=mock_open, read_data="supersecret")
    def test_get_secret_or_env_value_with_secret(self, mock_file):
        from launch import get_secret_or_env_value
        
        # Test secret retrieval
        result = get_secret_or_env_value("GAME_PASSWORD")
        self.assertEqual(result, "supersecret")
        mock_file.assert_called_once_with("/run/secrets/game_password", 'r')

    @patch.dict(os.environ, {"GAME_PASSWORD": "simple_password"})
    def test_get_secret_or_env_value_without_secret(self):
        from launch import get_secret_or_env_value
        
        # Test direct environment variable value
        result = get_secret_or_env_value("GAME_PASSWORD")
        self.assertEqual(result, "simple_password")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_secret_or_env_value_not_defined(self):
        from launch import get_secret_or_env_value
        
        # Test for undefined variable
        result = get_secret_or_env_value("GAME_PASSWORD")
        self.assertIsNone(result)

# Unit test for steamcmd_install with mocked install

class TestSteamCmdInstall(unittest.TestCase):
    
    @patch('subprocess.call')
    @patch.dict(os.environ, {"STEAM_APPID": "1234", "STEAM_USER": "user", "STEAM_PASSWORD": "password"})
    def test_steamcmd_install_with_login(self, mock_subprocess_call):
        from launch import steamcmd_install
        
        steamcmd_install()
        
        mock_subprocess_call.assert_called_once_with([
            "/steamcmd/steamcmd.sh",
            "+force_install_dir", "/reforger",
            "+login", "user", "password",
            "+app_update", "1234",
            "validate", "+quit"
        ])

    @patch('subprocess.call')
    @patch.dict(os.environ, {"STEAM_APPID": "1234"})
    def test_steamcmd_install_anonymous(self, mock_subprocess_call):
        from launch import steamcmd_install
        
        steamcmd_install()
        
        mock_subprocess_call.assert_called_once_with([
            "/steamcmd/steamcmd.sh",
            "+force_install_dir", "/reforger",
            "+login", "anonymous",
            "+app_update", "1234",
            "validate", "+quit"
        ])

# Unit test for generate_config

class TestGenerateConfig(unittest.TestCase):

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open, read_data='{"game": {}}')
    @patch.dict(os.environ, {"GAME_NAME": "TestGame"})
    def test_generate_config(self, mock_file, mock_exists):
        from launch import generate_config

        config_path = generate_config()
        # Verify the first call to open() for the default config
        mock_file.assert_any_call("/docker_default.json")
        # Verify that the generated config path is correct
        self.assertEqual(config_path, "/reforger/Configs/docker_generated.json")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"game": {}}')
    @patch.dict(os.environ, {"GAME_NAME": "TestGame", "ARMA_CONFIG": "docker_generated"})
    def test_generate_config_with_existing(self, mock_file, mock_exists):
        from launch import generate_config
        
        config_path = generate_config()
        # Check that open was called for the generated config file
        mock_file.assert_any_call("/reforger/Configs/docker_generated.json")
        # Verify that the generated config path is correct
        self.assertEqual(config_path, "/reforger/Configs/docker_generated.json")

# Finised :D