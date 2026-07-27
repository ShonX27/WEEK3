import sys
import importlib.util
print('python', sys.executable)
for name in ['streamlit', 'pandas', 'plotly']:
    print(name, bool(importlib.util.find_spec(name)))
    if importlib.util.find_spec(name):
        mod = __import__(name)
        print(name, getattr(mod, '__version__', 'unknown'))
