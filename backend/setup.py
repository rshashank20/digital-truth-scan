from setuptools import setup, find_packages

setup(
    name="digital-truth-scan-backend",
    version="1.0.0",
    description="AI Content Detection Backend",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-multipart==0.0.6",
        "transformers==4.35.2",
        "torch==2.1.1",
        "ffmpeg-python==0.2.0",
        "Pillow==10.1.0",
        "opencv-python==4.8.1.78",
    ],
    python_requires=">=3.11",
)
