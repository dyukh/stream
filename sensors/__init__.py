import importlib
from pathlib import Path
from sensors.base_sensor import Sensor

def load_sensors():
    sensors = {}
    for file in Path(__file__).parent.glob("*.py"):
        if file.name != "__init__.py" and file.name != "base_sensor.py":
            module_name = file.stem
            module = importlib.import_module(f"sensors.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Sensor) and attr != Sensor:
                    sensors[module_name] = attr
    return sensors
