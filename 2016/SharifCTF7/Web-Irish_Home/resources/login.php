<?php

session_start();

if (!empty($_SESSION['logged_in']))
	header('Location: /index.php');

require_once('header.php');

$text = "That account doesn't seem to exist";

if($_SERVER['REQUEST_METHOD'] == 'POST') 
{
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
			$conn->close();
		}
	}
		echo "<ul class=\"messages\"><li class=\"error\">$text</li></ul>";
}
?>

				<form action="/login.php" method="POST">
					<div class="mdl-textfield mdl-js-textfield">
						<input class="mdl-textfield__input" type="text" id="username" name="username">
						<label class="mdl-textfield__label" for="username">Username</label>
					</div><br/>
					<div class="mdl-textfield mdl-js-textfield">
						<input class="mdl-textfield__input" type="password" id="password" name="password">
						<label class="mdl-textfield__label" for="password">Password</label>
					</div><br/>
					<div style="text-align: center;" class="mdl-textfield mdl-js-textfield">
						<button class="btn waves-effect waves-light" type="submit">Submit</button>
					</div>
				</form>

<?php
require_once('footer.php');
?>
