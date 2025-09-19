import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.transform_utils import transformar_fuente

def run():
    return transformar_fuente("Regalias")
