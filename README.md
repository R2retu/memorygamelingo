# Memory Game Lingo

Interactive memory game built with **Python + Flet**.

## Features
- Human vs AI player (RoboKob)
- Multiple difficulty levels
- Animal sounds and images
- Memory AI that remembers cards

## Tech stack
- Python
- Flet
- MVC architecture

## Run locally

```bash
pip install -r requirements.txt
python main.py# Memory Game (Fleting Architecture)

A "Human vs Robokob" memory game built with Flet, refactored into a click-driven Fleting MVC architecture.

## Architecture Structure (Fleting)
This project enforces a clean separation of concerns:
- **`app.py` & `main.py`**: Entry points establishing the App shell and `Flet.run`, managing multi-route Views navigation.
- **`views/`**: Contains Flet UI definitions (`HomeView`, `GameView`, `ResultsView`). These depend on Models to read data, and call Controllers to invoke logic.
- **`controllers/`**: Coordinates logic (`GameController`, `RobokobController`). Updates observable models.
- **`models/`**: Observable data structures (`GameState`, `Card`, `PlayerState`, `Deck`). 
- **`services/`**: Abstracts heavy or infra operations (`AudioService`, `AssetService`).
- **`shared/`**: Common UI components and Theme specifications.

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Assets must be present in the `assets/` directory (e.g. `assets/imagesp/...`, `assets/audio/...`).

## Running Locally
```bash
python main.py
```
This runs the game using `flet.run()` on port `8080` (or the port defined in `$PORT`).

## Deploying to Cloud Run
Deploying the memory game to Cloud Run using Docker is straightforward since assets are bundled locally.
1. Make sure your `Dockerfile` exposes `8080` and runs `python main.py`.
2. Build and deploy to Google Cloud Run:
   ```bash
   gcloud run deploy memory-game --source . --port 8080 --allow-unauthenticated
   ```
