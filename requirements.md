# Package Requirements

Minimal dependencies for Flask database diagram generation.

## requirements.txt

```
Flask>=3.0.3
Flask-SQLAlchemy>=3.1.1
SQLAlchemy>=2.0.30
eralchemy2>=1.4.1
python-dotenv>=1.0.1
Flask-Migrate>=4.0.7
```

## Pipfile (Alternative)

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-sqlalchemy = "*"
sqlalchemy = "*"
eralchemy2 = "*"
python-dotenv = "*"
flask-migrate = "*"

[dev-packages]

[scripts]
init-db = "python src/app.py"
diagram = "eralchemy2 -i 'sqlite:///database.db' -o diagram.png"

[requires]
python_version = "3.8"
```

## Installation Commands

### Using pip

```bash
pip install -r requirements.txt
```

### Using pipenv

```bash
pipenv install
pipenv run init-db
pipenv run diagram
```

## Optional Dependencies

For enhanced functionality:

```
# Additional packages for production apps
python-dotenv>=1.0.1    # Environment variables
flask-migrate>=4.0.7    # Database migrations
pillow>=10.0.0          # Image processing (for better diagrams)
```

## Platform-Specific Notes

### macOS

```bash
# If you get installation errors
brew install graphviz
pip install eralchemy2
```

### Ubuntu/Debian

```bash
sudo apt-get install graphviz graphviz-dev
pip install eralchemy2
```

### Windows

```bash
# Install via conda for easier graphviz setup
conda install graphviz
pip install eralchemy2
```

## Verification

Test your installation:

```python
# test_install.py
try:
    import flask
    import flask_sqlalchemy
    import eralchemy2
    print("✅ All packages installed successfully!")
    print(f"Flask: {flask.__version__}")
    print(f"SQLAlchemy: {flask_sqlalchemy.__version__}")
    print(f"eralchemy2: {eralchemy2.__version__}")
except ImportError as e:
    print(f"❌ Missing package: {e}")
```
