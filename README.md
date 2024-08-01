# Suave supernovae

<img src="/Team Banner.png">

>In the fast-paced world of Discord, managing and making sense of extensive text conversations can be challenging.
>As the volume of messages grows, it becomes increasingly difficult to stay informed and engaged in discussions.
>Our solution addresses this problem with a bot designed to streamline and simplify text management on Discord.


Welcome to the code repository of 'Suave Supernovae' for the Python Discord Code Jam 2024!

We are excited to present our Discord Text Management Bot. As communication on Discord grows more complex, traditional methods for managing and understanding conversations can become inadequate. This challenge can make it difficult for users to stay informed and engaged, especially in active or large servers.

Our approach introduces features designed to enhance conversation management.

This approach aims to alleviate the difficulties associated with text overload and improve the overall experience of managing and participating in Discord discussions.


## Contents

This README consists of the following sections:

- [Contents](#contents)
- [Features](#features)
- [User Guide](#user-guide)
- [Installation](#installation)
- [How to Run the Project](#how-to-run-the-project)
- [Contributors](#contributors)

## Features

Our project has the following key features:

- `/summarize` :**AI-powered summarizer** that delivers a **concise summary** of conversations in any text channel, allowing users to quickly grasp ongoing discussions.
- `/ask` :**Ask the bot** feature lets users query the bot about any topic, even if it hasn’t been mentioned in the current conversation, avoiding the need to search through past messages or leave Discord.
- `/search` :Gives users the ability to **fetch Wikipedia articles** on specific topics directly within the Discord channel, providing instant access to relevant information.
- **Message saver** functionality enables users to **save and retrieve important messages** swiftly, ensuring easy access to critical information.
- `/help` :**Help command** offers descriptions of all available commands, helping users understand and utilize the bot’s features effectively.

## User Guide

Before you can use the discord bot, there are some setup steps you need to follow. This ensures the application works flawlessly on your local machine.


### Prerequisites

1. **Installation**: Before anything else, you need to set up the environment. Please follow our detailed [installation](#installation) guide to get everything in place.

2. **Running the bot**: Once installed, the next step is to start the bot.  please follow the guide on [how to run the project](#how-to-run-the-project).

### Using the App

With the application up and running, you can now explore the discord bot's capabilities:

1. To save messages simply select your message of choice and when the context menu pops up you should see a section named apps. Inside of that section you should see the ability to save a message.

<img src="./screenshots/savemessage.gif" alt="Saving messages with the discord application." width = "50%"></img>

2. To view your saved messages, click on the bot's icon, go to apps and select see saved messages.

 <img src="./screenshots/seesaves.png" alt="Seeing Saved messages with the discord application." width = "50%"></img>

3. If you want to use the summarizer command, run '/summarizer' in the thread or channel you want summarized.

<img src="./screenshots/summarizer.png" alt="Summarizing messages in a thread or channel." width = "50%"></img>

4. To use the ask command so that you can ask a question based on the chat or outside of chat, run '/ask'.

<img src="./screenshots/asknocontext.png" alt="Running the ask command in a thread or channel." width = "50%"></img>


5. For bringing up wikipedia articles in the chat, run '/wikisearch'.

<img src="./screenshots/wikisearch.png" alt="Bringing up wikipedia articles." width = "50%"></img>

6. If you ever forget the usage of a commmand, run '/help' to get a description of all of the commands.

<img src="./screenshots/help.PNG" alt="Help command showcase" ></img>



## Installation

Below are instructions on various ways to install this project. You can choose to either:

1. [Set up a local development environment](#local-installation), or
2. [Use the provided development container](#dev-container-installation) (requires Docker)

### Local Installation

To develop this project on your local machine, follow the steps outlined below.

> **Note**: Ensure you have Python version 3.11 installed. If not, download it from [here](https://www.python.org/downloads/).

To install the project locally you first need to run the following line to install all of its requirements

```
pip install -r requirements.txt
```

### Dev Container Installation

> **Note**: Due to last minute implementations you will have to rename env.local to .env.local in the docker file if you wish to use this approach


This project includes a [development container](https://containers.dev/) to simplify the setup process and provide a consistent development environment.

You can use the dev container locally with either [Visual Studio Code](#visual-studio-code) or [PyCharm](#pycharm), or remotely with [GitHub Codespaces](#github-codespaces).

#### Visual Studio Code

> **Note**: The following instructions assume that you have already installed [Docker](https://www.docker.com/) and [Visual Studio Code](https://code.visualstudio.com/).

1. Install the [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) in Visual Studio Code.

2. Make sure the Docker agent is running, and open Visual Studio Code.

3. Press `F1` to open the command palette, and then type "Dev-Containers: Clone Repository in Container Volume" and select it from the list. Alternatively, you can click on the green icon in the bottom-left corner of the VS Code window and select "Dev-Containers: Clone Repository in Container Volume" from the popup menu.

4. Next, the command palette will ask you for the repository URL. Copy the URL of the GitHub repository, paste it into the command palette and confirm by pressing `Enter`.

5. VS Code will automatically build the container and connect to it. This might take some time for the first run as it downloads the required Docker images and installs extensions.

6. Once connected, you'll see "Dev Container: Suave Supernova" in the bottom-left corner of the VS Code window, indicating that you are now working inside the container.

7. You're all set! You can now run, develop, build, and test the project using the provided development environment.

#### PyCharm

To connect PyCharm to the Development Container, please [follow these instructions](https://www.jetbrains.com/help/pycharm/connect-to-devcontainer.html) provided in the official JetBrains documentation.

#### GitHub Codespaces

1. Ensure that you have access to [GitHub Codespaces](https://github.com/features/codespaces).

2. Navigate to the GitHub repository for the project.

3. Click the "Code" button and then select "Open with Codespaces" from the dropdown menu.

4. Click on the "+ New codespace" button to create a new Codespace for the project.

5. GitHub Codespaces will automatically build the container and connect to it. This might take some time for the first run as it downloads the required Docker images and installs extensions.

6. Once connected, you'll see "Dev Container: Suave Supernova" in the bottom-left corner of the VS Code window, indicating that you are now working inside the container.

7. You're all set! You can now run, develop, build, and test the project using the provided development environment.


## How to Run the Project
1. For running this project you will need a discord bot token by getting it from the [discord developer portal](https://discord.com/developers/applications ). Follow the instructions on there to also add the bot to the server of your choosing.

2. You will also need a groq token which you can get from [here](https://console.groq.com/keys).

3. If you have installed the project locally you will also need to add a database dsn which can be done by running a postgres database and getting its connection string.

You can also use [neon](https://neon.tech/) to get your dsn.

4. You will now need to go the env.py file located in 'src/utils/env.py and rename '.env.local' to '.env'

5. Your .env file should now look something like this.

<img src="./screenshots/env.png" alt="example .env file"></img>

5. After having added the tokens and the database dsn to your .env file you can now run the bot on the server you've added it to.

If you installed the project locally you can run the project by running the following line in the root of the project.
```
python -m src
```

or alternatively you can run the bot using the container that was provided.

## Contributors

This project was built by `Suave Supernovae` team as part of the Python Discord Code Jam 2024. These are the team members and their main contributions:

| Avatar                                                     | Name                                        | Main contributions            |
| ---------------------------------------------------------- | ------------------------------------------- | ----------------------------- |
| <img src="https://github.com/Aekardy.png" width="50">   | [Aekardy](https://github.com/Aekardy) |  ask command   |
| <img src="https://github.com/kian3158.png" width="50">     | [Adrian Carton De Wiart](https://github.com/kian3158)  | search command, help command |
| <img src="https://github.com/theredditbandit.png" width="50"> | [TheLastMethBender](https://github.com/theredditbandit)     | summarizer and ask command, groq integration  |
| <img src="https://github.com/NaviTheCoderBoi.png" width="50">     | [NaviTheCoderBoi](https://github.com/NaviTheCoderboi)      | bot starter code, database setup       |
| <img src="https://github.com/Shubham-Mate.png" width="50">  | [Butter Dog](https://github.com/Shubham-Mate)   | message saver, database setup   |
