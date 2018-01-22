# Web - Vulnshop

```
We're preparing a website for selling some important vulnerabilities in the future. You can browse some static pages on it, waiting for the official release.

http://vulnshop.teaser.insomnihack.ch
```

This challenge was quite easy to understand, a little bit trickier to solve. The source of the `index.php` file was given and is available [here](https://github.com/YoloSw4g/writeups/blob/master/2018/Insomni'hack-Teaser-2018/web-vulnshop/resources/index.php).
There are 3 different actions that will interest us:
* **Contact us**, which sets an arbitrary value for your `$_SESSION['challenge']` variable
* **Captcha**, which creates a file in the `./tmp` directory, with the name of your challenge, and echoes back its value
* **Captcha-verify**, which allows you to execute an arbitrary PHP function, with first argument being `./<challenge>`, and second argument user-controled

However, things may not be simple to exploit since many sensitive PHP functions are disabled:
![PHPdisfun](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2018/Insomni'hack-Teaser-2018/web-vulnshop/resources/phpinfo.png)

Some writeups out there try (and succeed) in modifying the value of the session variable, by modifying the file where it is stored on-disk. We tried a different approach, since the `popen` function was not disabled:
```
resource popen ( string $command , string $mode )
```

In order to execute some arbitrary function, you have to call `/?page=captcha-verify&method=<function>&answer=<arg>`, which in turn will be resolved as `<function>('./<challenge>', '<arg>')`.
These are the different calls we made to get a reverse shell:

| Page | Method | Answer | Goal |
|:----:|:------:|--------|------|
| contact-us | N/A | N/A | Generate the random token |
| captcha | N/A | N/A | Create the file in `./tmp` |
| captcha-verify | `file_put_contents` | some bash reverse shell | Store a reverse shell in our file |
| captcha-verify | `chmod` | 511 | Sets chmod 0777 (octal, 511 in decimal) on our file |
| captcha-verify | `popen` | r | Launches the program |