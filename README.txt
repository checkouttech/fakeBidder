
Hello, World! Readme

Clean 
	python setup.py clean


Build RPM ( only on Linux box ) 
	
	python setup.py bdist_rpm
        python setup.py bdist_rpm --spec-only  
        python setup.py bdist_rpm --requires=python-bottle,supervisor,python-requests  --release=2
        python setup.py bdist_rpm --requires=python-bottle,supervisor,python-requests  --release=`git rev-list --count --first-parent HEAD`

        # Important : --python ensure the package portability to a regular python env
        python setup.py bdist_rpm  --python=&quot;/usr/bin/python&quot

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

        Using fakebidderctl 
		sudo sh /etc/init.d/fakebidderctl  start all
		sudo sh /etc/init.d/fakebidderctl  stop all


Run pytest
        
	Stand alone 
                py.test -v  --cov=fakebidder  --cov-report html  --cov-report xml --junitxml results.xml  --html=report.html

      	As part of setup.py 
		 python setup.py test -a "-v  --cov=fakebidder   --cov-report html --cov-report xml --junitxml results.xml  --html=report.html" 

Start using control file 

	sh /etc/init.d/fakebidderctl start all


yum 
	search for packages 
		 yum search bottle
		yum reinstall python-bottle




sonar notes 
	#wget http://repo1.maven.org/maven2/org/codehaus/sonar/runner/sonar-runner-dist/2.4/sonar-runner-dist-2.4.zip .
	# /home/vagrant/sonar/sonarqube-5.1.2/bin/linux-x86-64/sonar.sh restart
	# /home/vagrant/sonar/sonar-runner-2.4/bin/sonar-runner
	# sed -i 's/filename="/filename=".\//g' coverage.xml


pip notes 

	pip freeze


# /home/vagrant/sonar/sonar-runner-2.4/bin/sonar-runner sonar-project.properties

#  pylint --rcfile=pylint.cfg $(find handlers -maxdepth 1 -name "*.py" -print)  --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint.log || exit 0


# to get the files associated with the package 
rpm -ql  fakebidder
rpm -qlp package.rpm 

