# Motor del universo

- `universe.py`: coordina astronomía, planetas, química y vida.
- `world_time.py` y `simulation.py`: año simulado y avance con tiempo real.
- `save_manager.py`: persistencia de universos en `saves/`, desde la raíz del
  proyecto; conserva el formato JSON existente.
- `events.py`: sucesos registrados.
- `cosmology.py`: parámetros cosmológicos que usa la formación estelar.

`main.py` y `game.py` siguen en la raíz como entradas del programa. Los
imports ahora usan las rutas de estos paquetes; la lógica del motor permanece.
