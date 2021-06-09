# MicroChessPlayer

Game player for MicroChess AI

## Dependencies

This project uses pipenv. Note the following: [Version](Pipfile), [Modules](Pipfile.lock)

## Usage

1. Install pipenv

    ```
    pip install pipenv
    ```

1. Install all other dependencies

    ```
    pipenv install
    ```

### Run Player

3. Activate virtual environment

    ```
    pipenv shell
    ```

3. Run Player

    ```
    python src/main.py --port [PORT(default: 8000)] --url_env [URL of MicroChess API Server]
    ```

### Run Tests

3. Install dependencies for dev mode

    ```
    pipenv install -dev
    ```

3. Activate virtual environment

    ```
    pipenv shell
    ```

3. Run tests

    ```
    pytest test
    ```

## API Docs

After run player, navigate to the following url in your browser: http://localhost:8000/docs
