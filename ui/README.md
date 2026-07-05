# 🧩 Sliding Puzzle (Professional MVC Edition)

![Sliding Puzzle Gameplay Placeholder](assets/screenshots/gameplay.png)
*(Placeholder: Add screenshot of gameplay here)*

A highly polished, production-ready desktop implementation of the classic Sliding Puzzle (Taquin), built with **Python 3.11+** and **PySide6**. 

## ✨ Features
- **Multiple Difficulties**: Play in 3x3, 4x4, or 5x5 grid modes.
- **Solvable Shuffling Guarantee**: Uses a custom algorithm to perform 400-600 random, legal moves from a solved state, ensuring the puzzle is always solvable.
- **Builtin Procedural Themes**: Beautifully generated `Gradient`, `Sunset`, and `Forest` themes using advanced `QPainter` rendering. No external images required!
- **Custom Image Loading**: Load your own `.png`, `.jpg`, or `.bmp` files.
- **Real-Time Timer & Move Counter**: Keep track of your performance.
- **Live Preview**: Permanent 90x90 live preview of the target image.
- **Robustness**: Complete exception handling ensuring zero crashes, invalid move detection, and smooth O(1) grid state lookups.

---

## 🏗️ Clean Architecture (MVC/Services)
This application was engineered using enterprise-grade structural patterns to ensure maintainability, scalability, and strict separation of concerns.

```text
UI Layer (Widgets, Dialogs)
      ↓
Controllers (GameController, UIController)
      ↓
Services (Movement, Shuffle, Victory, Board, Image)
      ↓
Models (TileModel, BoardModel, MoveModel, GameState)
```
- **Models**: Pure DataClasses optimized for O(1) lookup. Zero UI logic.
- **Services**: Pure business logic (e.g., adjacency calculation, victory checking).
- **Controllers**: The glue that handles PySide6 signals and state mutations.
- **UI**: Strictly presentation widgets.

---

## 🚀 Installation & Launch

### Prerequisites
- Python 3.11 or newer.
- Git (optional).

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Run Tests
The project includes a test suite for core game logic:
```bash
python -m unittest discover tests/
```

---

## 🗺️ Roadmap / Future Enhancements
- [ ] **Fluid Animations**: Integrate `QPropertyAnimation` for smooth tile sliding.
- [ ] **A* Solver**: Implement an AI bot to auto-solve the puzzle.
- [ ] **Leaderboards**: Add SQLite database to track fastest times and lowest moves.
- [ ] **Sound Effects**: Integrate `QSoundEffect` for tile movements and victory chimes.

---
*Developed with strict adherence to SOLID principles and Clean Architecture.*
