from setuptools import setup
from setuptools.command.test import test as TestCommand

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

setup(
    name='fakebidder',
    version='0.15',
    license='BSD',
    author='gyeh',
    author_email='hello@world.com',
    url='http://www.hello.com',
    long_description="README.txt",
    install_requires=['bottle','requests','supervisor'],  # currently not working
    #dependency_links = ['https://pypi.python.org/packages/source/b/bottle/bottle-0.12.8.tar.gz'],
    packages=['fakebidder', 'fakebidder.images','fakebidder.docs'],
    include_package_data=True,
    package_data={'fakebidder.images' : ['hello.gif']},
    data_files=[
                ('/etc/init.d/', ['fakebidderctl']),
		('/var/log/fakebidder',[]),
                ('/etc/fakebidder/conf/',['conf/supervisord.conf'])
                ],
    description="Hello World testing setuptools",
    tests_require=['pytest'],
    cmdclass = {'test': PyTest}
)

#data_files=[('config', ['fakebidder/conf/supervisord.conf']),('/etc/init.d', ['init-script'])],
