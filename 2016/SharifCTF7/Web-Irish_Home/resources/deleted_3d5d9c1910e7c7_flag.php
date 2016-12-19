<?php

$username = 'Cuchulainn';
$password = ;	// Oi don't save me bleedin password in a shithole loike dis.

$salt = 'd34340968a99292fb5665e';

$tmp = $username . $password . $salt;
$tmp = md5($tmp);

$flag = "SharifCTF{" . $tmp . "}";

echo $flag;
?>
