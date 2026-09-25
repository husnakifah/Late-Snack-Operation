# Late Snack Operation — modular version

First Draft:
[![Draft Game](assets/draft-thumbnail.png)](ASSETS/initial_demo.mp4)

Final Gameplay:
[![Demo Game](assets/demo-thumbnail.png)](ASSETS/demo.mp4)

Struktur:
- `main.py` — entry point
- `config.py` — konfigurasi, konstanta, peta, dan data game
- `utils.py` — helper asset loading, collision, dan line-of-sight
- `ui.py` — popup UI
- `player.py` — class Player
- `clerk.py` — class Clerk / AI penjaga
- `game.py` — game state, event loop, update, dan rendering

Jalankan:
```bash
pip install pygame
python main.py
```
