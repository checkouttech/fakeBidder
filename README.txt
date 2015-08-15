
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
                py.test -v  --cov=fakebidder  --cov-report html  --cov-report xml --junitxml results.xml  --html=report.html

      	As part of setup.py 
		 python setup.py test -a "-v  --cov=fakebidder   --cov-report html --cov-report xml --junitxml results.xml  --html=report.html" 

#wget http://repo1.maven.org/maven2/org/codehaus/sonar/runner/sonar-runner-dist/2.4/sonar-runner-dist-2.4.zip .

# /home/vagrant/sonar/sonarqube-5.1.2/bin/linux-x86-64/sonar.sh restart
# /home/vagrant/sonar/sonar-runner-2.4/bin/sonar-runner
# sed -i 's/filename="/filename=".\//g' coverage.xml


# /home/vagrant/sonar/sonar-runner-2.4/bin/sonar-runner sonar-project.properties

