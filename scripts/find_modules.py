# Create a file named find_modules.py in VS Code
from modulefinder import ModuleFinder

finder = ModuleFinder()
finder.run_script('test_fk_rotation_invariance.py')

print('Loaded modules:')
for name, mod in finder.modules.items():
    print(f'{name}: {mod.__file__}')