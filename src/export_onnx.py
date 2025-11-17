from transformers import AutoTokenizer, AutoModel
from pathlib import Path
import os

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EXPORT_PATH = Path("models/miniLM_onnx")

# Make folder
os.makedirs(EXPORT_PATH, exist_ok=True)

print("📦 Loading model & tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

print("🔄 Exporting ONNX...")

from transformers.onnx import export
from transformers.onnx.features import FeaturesManager

feature = "feature-extraction"
model_kind, model_onnx_config = FeaturesManager.check_supported_model_or_raise(
    model, feature=feature
)
onnx_config = model_onnx_config(model.config)

export(
    preprocessor=tokenizer,
    model=model,
    config=onnx_config,
    opset=13,
    output=EXPORT_PATH / "model.onnx"
)

print("✅ ONNX Export Completed!")
print(f"Saved to: {EXPORT_PATH.resolve()}")
