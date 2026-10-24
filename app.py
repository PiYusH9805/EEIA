"""Run with: python -m streamlit run app.py"""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).parent / 'frontend' / 'streamlit_app.py'), run_name='__main__')
