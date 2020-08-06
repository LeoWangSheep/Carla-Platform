import os
import importlib
import sys
path_str = "D:/python_project/992_project/Carla-based Testing Platform/Carla-Platform/DrivingAgent/DetectAgent.py"

module_name = os.path.basename(path_str).split('.')[0]
print(module_name)
dir_path = os.path.dirname(path_str)
print(dir_path)
sys.path.insert(0, dir_path)
module_agent = importlib.import_module(module_name)

agent_class_name = module_agent.__name__

print(agent_class_name)

agent_instance = getattr(module_agent, agent_class_name)

print(agent_instance)

agent_instance.done(agent_instance)