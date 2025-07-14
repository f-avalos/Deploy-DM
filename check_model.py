import os
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def check_model_file(model_path='best_model.pkl'):
    """Check if the model file exists and report its details"""
    abs_path = os.path.abspath(model_path)
    
    logger.info(f"Checking for model file at: {abs_path}")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path)
        logger.info(f"✅ Model file exists! Size: {file_size} bytes")
        return True
    else:
        logger.error(f"❌ Model file NOT found at {abs_path}")
        # List all files in current directory
        files = os.listdir(".")
        logger.info(f"Files in current directory: {files}")
        return False

if __name__ == "__main__":
    model_path = 'best_model.pkl'
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    
    success = check_model_file(model_path)
    if not success:
        sys.exit(1)
