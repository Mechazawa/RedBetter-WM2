RedBetter-WM2
-----------------
Redbetter does not scrape the better.php HTML. This means that it's fine to use.

```
usage: redbetter-wm2 [-h] [-s SNATCHES] [-b BETTER] [-c COUNT] [-y YEAR]
                     [-w WAIT] [--320] [--V0] [--config CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -s SNATCHES, --snatches SNATCHES
                        minimum amount of snatches required before transcoding
                        (default: 5)
  -b BETTER, --better BETTER
                        better transcode search type (default: 3)
  -c COUNT, --count COUNT
                        maximum amount to queue (-1 for infinite) (default: 5)
  -y YEAR, --year YEAR  minimum release year (default: 2016)
  -w WAIT, --wait WAIT  wait X seconds between snatches (default: 3)
  --320                 Require 320 to be missing (default: False)
  --V0                  Require V0 to be missing (default: False)
  --config CONFIG       the location of the configuration file (default:
                        /Users/shodan/.config/redbetter)
```

## Example output

```
$ ./redbetter-wm2.py --year 2010 -s 1
Authenticating
Grabbing better list
1/5 Snatching [96548] Alex Anwandter - Amiga (2016) | Se 11 Le 0 Sn 3
2/5 Snatching [271405] Reina del Cid - Let&rsquo;s Begin (2011) | Se 2 Le 0 Sn 2
3/5 Snatching [325775] Aradia Ensemble - Theatre Music 2 (2016) | Se 7 Le 0 Sn 2
4/5 Snatching [250444] HyunA (현아) - A Talk (2014) | Se 3 Le 0 Sn 1
Grabbing better list
5/5 Snatching [356234] Laughing Buddha - - Sacred Technology (Nano Rec.) (2010) | Se 1 Le 0 Sn 1
```

## Example config
```ini
[redacted]
username = 
password = 

[whatmanager]
username = 
password = 
url = https://seedbox.example.com/transcode/request
```