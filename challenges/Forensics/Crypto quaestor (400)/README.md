## Crypto quaestor

**Category :** Forensics

**Points :** 400

**Solves :** -

**Description :**
Find the key

**Hint :** 
- 25 point hint: Find the AES keys to decrypt the container

### Write-up

Extracting `7z` file, we have been given two files, which are  

- WinXPprox86sp3.vmem
- fun_stuff.tc

So, we're given memory dump. Using `volatility` helps, we first list out all processes.  

```
$ volatility -f WinXPprox86sp3.vmem pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x81042bd0 System                    4      0     63      267 ------      0                                                              
0xff339220 smss.exe                540      4      3       19 ------      0 2014-01-31 11:51:55 UTC+0000                                 
0xff323a90 csrss.exe               604    540     13      420      0      0 2014-01-31 11:51:56 UTC+0000                                 
0xff3ee5f0 winlogon.exe            628    540     22      601      0      0 2014-01-31 11:51:56 UTC+0000                                 
0xff3503f0 services.exe            672    628     15      266      0      0 2014-01-31 11:51:56 UTC+0000                                 
0xff35da68 lsass.exe               684    628     22      356      0      0 2014-01-31 11:51:56 UTC+0000                                 
0xff35e168 vmacthlp.exe            844    672      1       25      0      0 2014-01-31 11:51:56 UTC+0000                                 
0xff35ada0 svchost.exe             880    672     19      205      0      0 2014-01-31 11:51:56 UTC+0000                                 
0x80f186e8 svchost.exe             948    672     10      254      0      0 2014-01-31 11:51:57 UTC+0000                                 
0xff3f48c0 MsMpEng.exe            1044    672     14      258      0      0 2014-01-31 11:51:57 UTC+0000                                 
0x80e7b3c0 svchost.exe            1112    672     65     1293      0      0 2014-01-31 11:51:58 UTC+0000                                 
0xff3f7310 svchost.exe            1256    672      6       83      0      0 2014-01-31 11:52:00 UTC+0000                                 
0xff2ffac0 svchost.exe            1444    672     14      195      0      0 2014-01-31 11:52:04 UTC+0000                                 
0xff322278 explorer.exe           1592   1536     12      309      0      0 2014-01-31 11:52:05 UTC+0000                                 
0xff419c38 spoolsv.exe            1656    672     14      140      0      0 2014-01-31 11:52:07 UTC+0000                                 
0xff1e2020 VMwareTray.exe         1884   1592      1       52      0      0 2014-01-31 11:52:12 UTC+0000                                 
0xff1e1bc0 vmtoolsd.exe           1892   1592      3      131      0      0 2014-01-31 11:52:12 UTC+0000                                 
0xff1df518 msseces.exe            1900   1592      6      212      0      0 2014-01-31 11:52:12 UTC+0000                                 
0xff1b5370 vmtoolsd.exe            272    672      6      261      0      0 2014-01-31 11:52:17 UTC+0000                                 
0xff183c68 wuauclt.exe             428   1112      8      180      0      0 2014-01-31 11:52:22 UTC+0000                                 
0xff1535b0 imapi.exe               904    672      5      115      0      0 2014-01-31 11:57:34 UTC+0000                                 
0x80f835f0 TPAutoConnSvc.e        1404    672      5       99      0      0 2014-01-31 11:57:42 UTC+0000                                 
0x80e759e0 wscntfy.exe             460   1112      1       28      0      0 2014-01-31 11:57:50 UTC+0000                                 
0x80ef7948 TPAutoConnect.e         676   1404      1       61      0      0 2014-01-31 11:57:52 UTC+0000                                 
0xff177340 alg.exe                1344    672      6      105      0      0 2014-01-31 11:57:53 UTC+0000                                 
0xff168460 wpabaln.exe            2868    628      1       58      0      0 2014-01-31 11:59:09 UTC+0000                                 
0x80edc020 MpCmdRun.exe           3708   3672     11      199      0      0 2014-01-31 12:01:10 UTC+0000                                 
0xff13c7b8 TrueCrypt.exe          4072   1592      2      123      0      0 2014-01-31 12:02:19 UTC+0000
```

We noticed that `TrueCrypt.exe` process is existed. Furthermore, original `7z` contains `fun_stuff.tc` file, which we assumed that this file might be TrueCrypt container.

We failed to solve it on the competition day...

Well, back home, I tried to look at list of options that `volatility` offers us.  
Something surprised me....

```
$ volatility -f WinXPprox86sp3.vmem -h
Volatility Foundation Volatility Framework 2.6
Usage: Volatility - A memory forensics analysis platform.

Options:
  -h, --help            list all available options and their default values.
      ...
                truecryptmaster Recover TrueCrypt 7.1a Master Keys
                truecryptpassphrase     TrueCrypt Cached Passphrase Finder
                truecryptsummary        TrueCrypt Summary
      ...
```

a `wtf` moment then appear... well it is time to try it shall we?

```
$ volatility -f WinXPprox86sp3.vmem truecryptsummary
Volatility Foundation Volatility Framework 2.6
Process              TrueCrypt.exe at 0xff13c7b8 pid 4072
Service              truecrypt state SERVICE_RUNNING
Kernel Module        truecrypt.sys at 0xfd415000 - 0xfd44c000
Symbolic Link         -> \Device\TrueCryptVolumeQ mounted 2014-01-31 12:03:11 UTC+0000
Symbolic Link        Volume{e9d25d5d-8a5d-11e3-a46a-000c2990bf48} -> \Device\TrueCryptVolumeQ mounted 2014-01-31 12:03:11 UTC+0000
Driver               \Driver\truecrypt at 0x1bf2bc8 range 0xfd415000 - 0xfd44bb80
Device               TrueCryptVolumeQ at 0x80f9ea48 type FILE_DEVICE_DISK
Container            Path: \??\C:\fun_stuff
Device               TrueCrypt at 0x80eeed98 type FILE_DEVICE_UNKNOWN

$ volatility -f WinXPprox86sp3.vmem truecryptmaster
Volatility Foundation Volatility Framework 2.6
Container: \??\C:\fun_stuff
Hidden Volume: No
Removable: No
Read Only: No
Disk Length: 786432 (bytes)
Host Length: 1048576 (bytes)
Encryption Algorithm: AES
Mode: XTS
Master Key
0xff0f01a8  9b 08 18 01 e6 71 87 57 77 8e 77 cb 07 5b 71 56   .....q.Ww.w..[qV
0xff0f01b8  81 f7 fb fd 81 a6 da 7e d8 96 99 5a 79 74 0e d9   .......~...Zyt..
0xff0f01c8  84 65 95 89 44 37 a5 27 33 3d c4 4d ad 10 9d 2f   .e..D7.'3=.M.../
0xff0f01d8  7b e8 3d bf ca be f5 de 73 89 7a cc 2f b8 cc a4   {.=.....s.z./...
```

As we can see, the master key of TrueCrypt easily appeared there.

So, I looked online, and found out this tool [MKDecrypt](https://github.com/AmNe5iA/MKDecrypt), which can provide us functionality to decrypt the container with the master key.

Without further ado:
  
```
# sudo python MKDecrypt.py ../fun_stuff.tc "9b081801e6718757778e77cb075b715681f7fbfd81a6da7ed896995a79740ed9846595894437a527333dc44dad109d2f7be83dbfcabef5de73897acc2fb8cca4"
[sudo] password for shahril: 
 
Normal/outer volume found in ../fun_stuff.tc using aes-xts-plain64 
../fun_stuff.tc is decrypted at /dev/mapper/MKDecrypt1
Once done, press Enter to dismount ../fun_stuff.tc...
```

Copying stuff into our dir, and `foremost`-ing it.

```
# cp /dev/mapper/MKDecrypt1 test
# foremost test
Processing: test
|foundat=secret_key.png�PNG
▒
*|
```

Woot. Looking at the `png` file give us the most-awaiting flag.

`A good key is hard to find!`