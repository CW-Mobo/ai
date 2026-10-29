from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRAINING_DIR = BASE_DIR / "treinamento"
ASSETS_DIR = BASE_DIR / "assets"
MODEL_PATH = TRAINING_DIR / "modelo_lichia.keras"
LOGO_PATH = ASSETS_DIR / "logo.png"
CSS_PATH = ASSETS_DIR / "styles.css"
IMG_HEIGHT = 224
IMG_WIDTH = 224
LAST_CONV_LAYER_NAME = "out_relu"
MAX_DISPLAY_CONFIDENCE = 0.982
