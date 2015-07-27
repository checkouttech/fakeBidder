
Hello, World! Readme

Build RPM ( only on Linux box ) 
	
	python setup.py sdist

Install RPM

	sudo yum install  fakebidder-0.13-1.noarch.rpm

Build Egg
	
	python setup.py sdist	

Install Egg 

	pip install fakebidder-0.13-1.tar.gz
 

Set python path 

	export PYTHONPATH=/usr/lib/python2.7/site-packages/fakebidder/

Supervisor

	supervisord -c supervisord.conf
	supervisorctl start long_script


