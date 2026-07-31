import unittest
import sys
import platform

class TestLibraries(unittest.TestCase):
    def test_pandas(self):
        import pandas as pd
        print(f"\n[PASS] Pandas imported successfully (v{pd.__version__})")
        self.assertIsNotNone(pd.__version__)

    def test_numpy(self):
        import numpy as np
        print(f"[PASS] NumPy imported successfully (v{np.__version__})")
        self.assertIsNotNone(np.__version__)

    def test_seaborn(self):
        import seaborn as sns
        print(f"[PASS] Seaborn imported successfully (v{sns.__version__})")
        self.assertIsNotNone(sns.__version__)

    def test_scikit_learn(self):
        import sklearn
        print(f"[PASS] Scikit-Learn imported successfully (v{sklearn.__version__})")
        self.assertIsNotNone(sklearn.__version__)

    def test_tensorflow_gpu(self):
        import tensorflow as tf
        print(f"[PASS] TensorFlow imported successfully (v{tf.__version__})")
        
        gpus = tf.config.list_physical_devices('GPU')
        system_os = platform.system()
        cpu_arch = platform.machine()
        
        print(f"       System: {system_os} ({cpu_arch})")
        
        if len(gpus) > 0:
            print(f"       TensorFlow GPU detected: {gpus}")
            # If running on macOS M-series, verify metal plugin is loaded
            if system_os == "Darwin" and cpu_arch == "arm64":
                print("       TensorFlow Metal/GPU acceleration is active.")
        else:
            print("       No TensorFlow GPU detected. Fallback to CPU-only execution.")
            if system_os == "Darwin" and cpu_arch == "arm64":
                print("       [WARNING] Running on Apple Silicon but TensorFlow Metal GPU not detected.")
        
        # Verify tensor operations complete successfully
        x = tf.random.normal([2, 2])
        y = x + x
        self.assertIsNotNone(y)

    def test_pytorch_gpu(self):
        import torch
        print(f"[PASS] PyTorch imported successfully (v{torch.__version__})")
        
        mps_available = torch.backends.mps.is_available()
        cuda_available = torch.cuda.is_available()
        system_os = platform.system()
        cpu_arch = platform.machine()
        
        # Determine acceleration device
        if mps_available:
            device_name = "mps"
            print("       PyTorch Acceleration: MPS (Metal Performance Shaders) is available.")
        elif cuda_available:
            device_name = "cuda"
            print(f"       PyTorch Acceleration: CUDA (NVIDIA GPU) is available: {torch.cuda.get_device_name(0)}")
        else:
            device_name = "cpu"
            print("       PyTorch Acceleration: None (using CPU).")
            if system_os == "Darwin" and cpu_arch == "arm64":
                print("       [WARNING] Running on Apple Silicon but PyTorch MPS not available.")
        
        # Run tensor operations on the best available device
        device = torch.device(device_name)
        x = torch.randn(2, 2, device=device)
        y = x + x
        print(f"       Successfully ran PyTorch tensor operations on: {device}")
        self.assertIsNotNone(y)

if __name__ == '__main__':
    unittest.main()
