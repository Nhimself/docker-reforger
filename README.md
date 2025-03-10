# This repo is a fork
of the official docker reforger script all code originates from that repo. Thanks: @acemod [acemod/docker-reforger:main](https://github.com/acemod/docker-reforger)
This image uses the official steamcmd and has some code optimizations, making it easier to read and test before launch.
Primary change is supporting [docker secrets](https://docs.docker.com/engine/swarm/secrets/) 

[![Build Docker image](https://github.com/Nhimself/docker-reforger/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Nhimself/docker-reforger/actions/workflows/docker-image.yml)  [![Build and publish to Docker](https://github.com/Nhimself/docker-reforger/actions/workflows/ghcr.yaml/badge.svg)](https://github.com/Nhimself/docker-reforger/actions/workflows/ghcr.yaml)

# For freedom fighers guild members
Please see the [freedom-fighers](https://github.com/Nhimself/docker-reforger/tree/main/freedom-fighters) folder for mods_list file and pre-made compose file

# Arma Reforger Dedicated Server

An Arma Reforger dedicated server. Updates to the latest version every time it is restarted.

## Usage

### Docker CLI

```sh
    docker create \
        --name=reforger-server \
        -p 2001:2001/udp \
        -v path/to/configs:/reforger/Configs \
        -v path/to/profiles:/home/profile \
        -v path/to/workshop:/reforger/workshop \
        -e SERVER_PUBLIC_ADDRESS="public ip" \
        -e GAME_NAME="My Docker Reforger Server" \
        ghcr.io/acemod/arma-reforger:latest
```

If an admin password is not provided, one will be generated and printed to the console.

### Docker-compose

Simply check-out / copy [the provided docker-compose.yml](docker-compose.yml) and adjust to your personal needs.

## Parameters

Check [the Dockerfile](Dockerfile#L32-L67), more docs will come later.

Build using buildx

`docker buildx build -f Dockerfile . --tag dockerreforger:buildx`

### Configs

By default the configs are generated from the ENV variables in the dockerfile. After the first run the file can be expanded with additional options manually, but the fields will always be overwritten by the ENV variables.

Alternatively, change the `ARMA_CONFIG` variable to a file present in the `Configs` volume. It will be used without modification.

### Experimental server

To use the experimental server instead of the regular set `STEAM_APPID` variable to `1890870`.

### Mods

Workshop mods can be defined in two ways. You can use both or either of those.

#### GAME_MODS_IDS_LIST

A comma separated list of IDs, with an optional version.

```sh
-e GAME_MODS_IDS_LIST="5965770215E93269=1.0.6,5965550F24A0C152"
```

#### GAME_MODS_JSON_FILE_PATH

Path to a JSON file that contains array of mod objects.

```sh
-v ${PWD}/mods_file.json:/mods_file.json
-e GAME_MODS_JSON_FILE_PATH="/mods_file.json" 
```

```json
[
  {
    "modId": "597706449575D90B",
    "version": "1.1.1"
  }
]
```
### RCON

RCON can be activated by defining the `RCON_PASSWORD` variable.

```sh
-e RCON_PASSWORD="ExamplePassword123"
```

The password:
* is required for RCON to start
* does not support spaces
* must be at least 3 characters long

Use `-e RCON_PERMISSION=""` to change [permission](https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#permission) for all RCON clients.