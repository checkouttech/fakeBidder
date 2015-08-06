
Hello, World! Readme

Build RPM ( only on Linux box ) 
	
	python setup.py bdist_rpm

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

Run pytest
        
	Stand alone 
		py.test -v  --cov=fakebidder   --cov-report html --junitxml results.xml  --html=report.html

      	As part of setup.py 
		 python setup.py test -a "-v  --cov=fakebidder   --cov-report html --junitxml results.xml  --html=report.html" 



