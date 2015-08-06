from setuptools import setup

setup(
    name='fakebidder',
    version='0.14',
    license='BSD',
    author='gyeh',
    author_email='hello@world.com',
    url='http://www.hello.com',
    long_description="README.txt",
    packages=['fakebidder', 'fakebidder.images','fakebidder.docs','fakebidder.conf'],
    include_package_data=True,
    package_data={'fakebidder.images' : ['hello.gif'],'fakebidder.docs' : ['supervisord.conf']},
    description="Hello World testing setuptools",
)
