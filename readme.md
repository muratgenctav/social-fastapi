# Settings for virtual environment
conda deactivate
source .venv/bin/activate

# Instantiate the virtual environment
python3 -m venv .venv
pip install -r requirements.txt

# Run the app server
uvicorn app.main:app --reload

# Database upgrade
1. Make the necessary change in models.py
2. Run cmd: alembic revision --autogenerate -m "<description>"
3. Run cmd: alembic upgrade <generated revision id>