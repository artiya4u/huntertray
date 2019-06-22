HunterTray
==========

HunterTray is a simple [ProductHunt](https://www.producthunt.com/) Linux application
that lets you view top ProductHunt in your System Tray.

The inspiration for this came from [HackerTray](https://github.com/captn3m0/HunterTray/).

## Screenshot

![HunterTray Screenshot in Ubuntu 18.04](https://imgur.com/JeFmnVq.png)

## Installation
HunterTray is distributed as a python package. Do the following to install:

``` sh
sudo pip install huntertray
OR
sudo easy_install huntertray
OR
#Download Source and cd to it
sudo python setup.py install
```

After that, you can run `HunterTray` from anywhere and it will run. You can
now add it to your OS dependent session autostart method. In Ubuntu, you can
access it via: 

1. System > Preferences > Sessions  
(OR)
2. System > Preferences > Startup Applications 

depending on your Ubuntu Version. Or put it in `~/.config/openbox/autostart` 
if you are running OpenBox.
On PopOs install this to display AppIndicator https://extensions.gnome.org/extension/615/appindicator-support/

### Upgrade
The latest stable version is [![the one on PyPi](https://pypip.in/v/huntertray/badge.png)](https://pypi.python.org/pypi/huntertray/)

You can check which version you have installed with `HunterTray --version`.

To upgrade, run `pip install -U huntertray`. In some cases (Ubuntu), you might
need to clear the pip cache before upgrading:

`sudo rm -rf /tmp/pip-build-root/huntertray`

HunterTray will automatically check the latest version on startup, and inform you if there is an update available.

## Options
HunterTray accepts its various options via the command line. Run `huntertray -h` to see all options. Currently the following switches are supported:

1. `-c`: Enables comments support. Clicking on links will also open the comments page on HN. Can be switched off via the UI, but the setting is not remembered.
2. `--chrome PROFILE-PATH`: Specifying a profile path to a chrome directory will make HunterTray read the Chrome History file to mark links as read. Links are checked once every 5 minutes, which is when the History file is copied (to override the lock in case Chrome is open), searched using sqlite and deleted. This feature is still experimental.
3. `--firefox PROFILE-PATH`: Specify path to a firefox profile directory. HunterTray will read your firefox history from this profile, and use it to mark links as read.

Note that the `--chrome` and `--firefox` options are independent, and can be used together. However, they cannot be specified multiple times (so reading from 2 chrome profiles is not possible).


### Google Chrome Profile Path

Where your Profile is stored depends on which version of chrome you are using:

- `google-chrome-stable`: `~/.config/google-chrome/Default/`
- `google-chrome-unstable`: `~/.config/google-chrome-unstable/Default/`
- `chromium`: `~/.config/chromium/Default/`

Replace `Default` with `Profile 1`, `Profile 2` or so on if you use multiple profiles on Chrome. Note that the `--chrome` option accepts a `PROFILE-PATH`, not the History file itself. Also note that sometimes `~` might not be set, so you might need to use the complete path (such as `/home/nemo/.config/google-chrome/Default/`).

### Firefox Profile Path
The default firefox profile path is `~/.mozilla/firefox/*.default`, where `*` denotes a random 8 digit string. You can also read `~/.mozilla/firefox/profiles.ini` to get a list of profiles.

## Features
1. Minimalist Approach to ProductHunt
2. Opens links in your default browser
3. Remembers which links you opened
4. Shows Points/Comment count in a simple format
5. Reads your Google Chrome History file to determine which links you've already read (even if you may not have opened them via HunterTray)

### Troubleshooting

If the app indicator fails to show in Ubuntu versions, consider installing 
python-appindicator with

`sudo apt-get install python-appindicator python-gtk2`

### Development

To develop on HunterTray, or to test out experimental versions, do the following:

- Clone the project
- Run `(sudo) python setup.py develop` in the HunterTray root directory
- Run `huntertray` with the required command line options from anywhere.

## Credits

- Abhay Rana for [HackerTray](https://github.com/captn3m0/hackertray/).

## Author Information
- Artiya Thinkumpang (<artiya4u@gmail.com>)

## Licence
Licenced under the [MIT Licence](http://nemo.mit-license.org/).

