import pkg_resources
from subprocess import call

# Mass update of all packages.. handle with care!.
packages = [dist.project_name for dist in pkg_resources.working_set]
call("pip install --upgrade " + ' '.join(packages), shell=True)