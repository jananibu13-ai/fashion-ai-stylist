from pyngrok import ngrok
import subprocess

public_url = ngrok.connect(8501)

print("Public URL:", public_url)

subprocess.run(
    ["streamlit", "run", "app.py"]
)