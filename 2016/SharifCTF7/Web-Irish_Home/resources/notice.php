<?php
if(!isset($_SESSION))
	session_start();

if (empty($_SESSION['logged_in'])) {
	header('Location: /login.php');
}

$root = realpath($_SERVER["DOCUMENT_ROOT"]);
require_once("$root/header.php");
?>


<div style="text-align: center;">
	<h2 style="color: red;">Important Notice</h2>

	<div style="line-height: 1cm; display: inline-block; text-align: left; font-size: 20px;">
		Ter de pesky contestants av dat bleedin darn SharifCTF:<br/><br/>

		Sum bugger deleted me beloved <kbd style='display:inline-block; margin:0 .1em; padding:.1em .6em; color:#242729; text-shadow:0 1px 0 #FFF; background-color:#e1e3e5; border:1px solid #adb3b9; border-radius:1px; box-shadow:0 1px 0 rgba(12,13,14,0.2),0 0 0 2px #FFF inset; white-space:nowrap'>flag.php</kbd> file.<br/>

		Oi want it back! not next week, not the-morra &mdash; roi nigh!<br/>

		An' be queck aboyt it, as naw opshuns is aff de table.<br/>

		Don't tell me lay-ra dat yer weren't warned.
	</div>
</div>
<?php
require_once("$root/footer.php");
?>