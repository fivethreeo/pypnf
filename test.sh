# create virtual environment if not exists

if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install pytest pytest-cov
    pip install -e .
else
    source venv/bin/activate
fi

# Run tests
pytest --cov=pypnf --cov-report=html tests/