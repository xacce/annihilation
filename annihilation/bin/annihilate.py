from annihilation.runner import AnnihilationRunner
import oyaml as yaml
import sys


path = sys.argv[1]
with open(path) as f:
    config = yaml.load(f.read())

runner = AnnihilationRunner(config)
runner.run()
