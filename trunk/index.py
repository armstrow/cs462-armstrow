from mod_python import apache
from mod_python import util

def index(req):
	req.content_type = "text/html"
	req.send_http_header()
	req.write('''
	<html>
	<head>
		<title>The Image Project</title>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-15" />
		<link rel="stylesheet" href="/style.css" />
	</head>
	<body>
	<div id="conteneur">

		  <div id="header">The Image Project</div>
		  
		  <div id="haut">
			<ul class="menuhaut">
				<li><a href="/">Home</a></li>
				<li><a href="/list/popular">Popular</a></li>
				<li><a href="/list/recent">Recent</a></li>

				<li><a href="/submit">Submit</a></li>
			</ul>
		  </div>

		  <div id="centre">
	<style>
	.thumblist {
		clear: both;
	}	
	.thumblist a {
			float: left;
			margin-right: 5px;
		}
	</style>
	<h1>Recent Images</h1>
	<div class="thumblist">
	</div>
	<br/>
	<a href="/list/recent">See more Recent Images</a>
	<br/><br/><br/>

	<h1>Popular Images</h1>

	<div class="thumblist">
	</div>
	<br/>
	<a href="/list/popular">See more Popular Images</a>
	<br/><br/><br/>

	<h1>About The Image Project</h1>
	<p>The Image Project is a simple website used in teaching cloud computing principles and techniques. 
	This project uses Python, EC2, SQS, SimpleDB, Cheetah, and jQuery.</p>

			  </div>
			<div id="pied">CS462 Server created by Sam. Design by <a href="http://nicolas.freezee.org">Nicolas Fafchamps</a></div>
		</div>
		</body>
	</html>
	''')


	return

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
