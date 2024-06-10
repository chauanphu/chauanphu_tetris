# The Blockbuster

- A simple tetris-based game that you can enjoy yourself or with your friends to see who can break the most blocks.

## Installation

1. Clone the repository: `git clone https://github.com/chauanphu/chauanphu_tetris.git`
2. Set up virtual environment: `python3 -m venv venv`
3. Install a dependencies: `pip install -r requirements.txt`

## Usage

1. Navigate to the project directory: `cd src`
2. Run the game: `python main.py`

## Controls

1. Choose the player mode:
    - Single player
    - Multiple player

- For single player:
  - The tetrominos will drop gradually and stacking up. If they reach the top, you will loose.
  - For each blocks that form a filled row, it will pop out, prevend you from getting to your demise (for now).
  - You can use the "◀️" and "▶️" to move the tetrominos horizontally.
  - 🔼 button does not move tetromino up but instead rotates it.
  - And if you can see the tetrominos fall not quickly enough, you can speed it up by pressing 🔽

- For multiple player:
  - The game logic would basically the same. However, you can create multiple users and compete with your friends for mastery of this game.

## Contributing

Contributions are welcome! If you'd like to contribute to The Legend of Fire Fox, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
