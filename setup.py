from setuptools import setup
from setuptools.command.test import test as TestCommand
from setuptools import setup, Command
import os 
import subprocess 

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.pytest_args)


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')



setup(
    name='fakebidder',
    version='0.15',
    # release is not supported in bdist rpm 
    release=subprocess.check_output(["git", "rev-list", "--count", "--first-parent", "HEAD"]).rstrip(),
    license='BSD',
    author='gyeh',
    author_email='hello@world.com',
    url='http://www.hello.com',
    long_description="README.txt",
    #install_requires=['bottle','requests','supervisor'],  # currently not working
    #dependency_links = ['https://pypi.python.org/packages/source/b/bottle/bottle-0.12.8.tar.gz'],
    packages=['fakebidder', 'fakebidder.images','fakebidder.docs'],
    include_package_data=True,
    package_data={'fakebidder.images' : ['hello.gif']},
    data_files=[
                ('/etc/init.d/', ['fakebidderctl']),
		('/var/log/fakebidder',[]),
                ('/etc/fakebidder/conf/',['conf/supervisord.conf','conf/fakebidder.conf'])
                ],
    description="Hello World testing setuptools",
    tests_require=['pytest'],
    cmdclass = {
                'test': PyTest,
                'clean': CleanCommand
                }

)

#data_files=[('config', ['fakebidder/conf/supervisord.conf']),('/etc/init.d', ['init-script'])],
