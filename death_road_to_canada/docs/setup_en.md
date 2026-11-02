# Death Road to Canada - Setup Guide

## What you need

- Death Road to Canada on Steam (TRACHEA branch or later)
- Python 3.6 or newer - [python.org/downloads](https://www.python.org/downloads/)
    - On Windows, tick **Add Python to PATH** during install
- Archipelago - [archipelago.gg](https://archipelago.gg/)
- The latest DR2C Archipelago release zip from the project page

## Install

1. Extract the release zip anywhere you like (Documents, Desktop, wherever)
2. Open a terminal in that folder
    - Windows: Shift + right-click inside the folder, "Open PowerShell window here"
    - Mac/Linux: right-click, "Open in Terminal"
3. Run:

    ```
    python setup.py
    ```

    (On Mac/Linux use `python3`.)

4. The script finds your DR2C install in the usual Steam locations. If it can't, it asks for the path - paste the folder that contains `deathforth/`.
5. It asks for your Archipelago install folder next. Paste the folder that contains `ArchipelagoLauncher`.
6. Done. The script copies mod files, installs the APWorld, and installs the Python libraries the client needs.

## Create your YAML

Grab the template YAML from the release zip (or export one from the Archipelago generator). Open it in a text editor.

Key options:

- `goal_modes` - which modes you need to beat to win. All listed must be cleared.
- `enabled_modes` - which modes get per-mode location checks. Goal modes are always enabled.
- The various `*_milestone_max` and `*_milestone_interval` settings control how many checks you get in each category.

Full option descriptions are in the template YAML comments.

Then either generate locally or upload your YAML to [archipelago.gg](https://archipelago.gg/) with the other players'.

## Playing

1. Launch Death Road to Canada
2. Pick **ARCHIPELAGO** from the main menu - **not** regular New Game
3. From the folder you extracted the release to, run:

    ```
    python DRTC_Client.py
    ```

4. Enter the server address, your slot name, and the room password if there is one
5. Hit Connect, then start a run in the game

Items from the multiworld arrive while you're on the road or in a mission. Checks fire as you play.

## Important

- **Save slot 1 is used by the mod.** Slots 2 and 3 stay vanilla. Don't manually save or load slot 1 outside Archipelago mode.
- **Progress is cumulative.** Dying doesn't reset your kill count, loot count, mode unlocks, or anything else.
- **Your trunk restocks every new run.** Items you've received from the multiworld get redelivered when you start a fresh run - that's how the integration keeps the roguelike feel.
- **Mid-run reconnects are safe.** If your wifi drops or the server restarts, items don't flood your current trunk. The client only redelivers on a genuine new run.

## Troubleshooting

**`python` is not recognised (Windows)**  
Python isn't on PATH. Easiest fix: reinstall Python from python.org and tick "Add Python to PATH" during install. Or use `py setup.py` instead.

**`setup.py` can't find my DR2C install**  
Enter the path manually when it asks. The path should be the folder that contains `deathforth/boot.df`. On Steam that's usually `C:\Program Files (x86)\Steam\steamapps\common\DeathRoadToCanada`.

**The mod doesn't load / `ARCHIPELAGO` option isn't in the menu**  
Open the game's console (backtick key) and look for the error. Usually means the mod files didn't copy properly. Rerun `setup.py`.

**"certificate has expired" error from the client**  
Your Python's SSL certificate bundle is out of date. Either run `pip install --upgrade certifi` in a terminal, or uncheck "Verify SSL certificate" in the client window.

**Items don't arrive**  
Check the client is connected (green status). Make sure the save path in the client matches your DR2C save folder - the client auto-detects but you can override it with the Browse button.

**I want to uninstall**  
Steam -> DR2C -> Properties -> Local Files -> Verify Integrity of Game Files. That restores the base game to vanilla.

## When a new branch update drops

DR2C branch updates (STOMACH, TRACHEA, UVULA, etc.) overwrite base game files with vanilla, which breaks the mod. When that happens, grab the next release and rerun `setup.py`. Your Archipelago progress isn't affected - only the mod code gets replaced.

## Save file locations

| OS | Path |
|---|---|
| Windows | `%APPDATA%\.madgarden\DR2C\` |
| Mac | `~/Library/Application Support/.madgarden/DR2C/` |
| Linux | `~/.madgarden/DR2C/` |

The client and mod communicate via text files there (`ap_inbox.txt`, `ap_outbox.txt`, `ap_status.txt`, `ap_session.txt`). Don't delete these while playing.
