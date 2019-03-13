#!/usr/bin/env python

from __future__ import print_function
import os
import requests
import platform
import subprocess
import json
import argparse
from os.path import expanduser
import signal

from producthunt import ProductHunt
from chrome import Chrome
from firefox import Firefox
from version import Version

if os.environ.get('TRAVIS') != 'true':
    import pygtk

    pygtk.require('2.0')
    import gtk

    import webbrowser

    try:
        import appindicator
    except ImportError:
        import appindicator_replacement as appindicator

    from appindicator_replacement import get_icon_filename


class HunterTrayApp:
    UPDATE_URL = "https://github.com/artiya4u/huntertray#upgrade"
    ABOUT_URL = "https://github.com/artiya4u/huntertray"

    def __init__(self, args):
        # Load the database
        home = expanduser("~")
        with open(home + '/.huntertray.json', 'a+') as content_file:
            content_file.seek(0)
            content = content_file.read()
            try:
                self.db = set(json.loads(content))
            except ValueError:
                self.db = set()

        # create an indicator applet
        self.ind = appindicator.Indicator("Hunter Tray", "hunter-tray", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon(get_icon_filename("hunter-tray.png"))

        # create a menu
        self.menu = gtk.Menu()

        # The default state is false, and it toggles when you click on it
        self.commentState = args.comments

        # create items for the menu - refresh, quit and a separator
        menuSeparator = gtk.SeparatorMenuItem()
        menuSeparator.show()
        self.menu.append(menuSeparator)

        btnComments = gtk.CheckMenuItem("Show Comments")
        btnComments.show()
        btnComments.set_active(args.comments)
        btnComments.connect("activate", self.toggle_comments)
        self.menu.append(btnComments)

        btnAbout = gtk.MenuItem("About")
        btnAbout.show()
        btnAbout.connect("activate", self.show_about)
        self.menu.append(btnAbout)

        btnRefresh = gtk.MenuItem("Refresh")
        btnRefresh.show()
        # the last parameter is for not running the timer
        btnRefresh.connect("activate", self.refresh, True, args.chrome)
        self.menu.append(btnRefresh)

        if Version.new_available():
            btnUpdate = gtk.MenuItem("New Update Available")
            btnUpdate.show()
            btnUpdate.connect('activate', self.show_update)
            self.menu.append(btnUpdate)

        btnQuit = gtk.MenuItem("Quit")
        btnQuit.show()
        btnQuit.connect("activate", self.quit)
        self.menu.append(btnQuit)

        self.menu.show()

        self.ind.set_menu(self.menu)
        self.refresh(chrome_data_directory=args.chrome, firefox_data_directory=args.firefox)
        self.launch_analytics(args)

    def launch_analytics(self, args):
        # Now that we're all done with the boot, send a beacone home
        launch_data = vars(args)
        launch_data['version'] = Version.current()
        launch_data['platform'] = platform.linux_distribution()
        try:
            launch_data['browser'] = subprocess.check_output(["xdg-settings", "get", "default-web-browser"]).strip()
        except subprocess.CalledProcessError as e:
            launch_data['browser'] = "unknown"

    def toggle_comments(self, widget):
        """Whether comments page is opened or not"""
        self.commentState = not self.commentState

    def show_update(self, widget):
        """Handle the update button"""
        webbrowser.open(HunterTrayApp.UPDATE_URL)
        # Remove the update button once clicked
        self.menu.remove(widget)

    def show_about(self, widget):
        """Handle the about btn"""
        webbrowser.open(HunterTrayApp.ABOUT_URL)

    # ToDo: Handle keyboard interrupt properly
    def quit(self, widget, data=None):
        """ Handler for the quit button"""
        l = list(self.db)
        home = expanduser("~")

        # truncate the file
        with open(home + '/.huntertray.json', 'w+') as file:
            file.write(json.dumps(l))

        gtk.main_quit()

    def run(self):
        signal.signal(signal.SIGINT, self.quit)
        gtk.main()
        return 0

    def open(self, widget, event=None, data=None):
        """Opens the link in the web browser"""
        # We disconnect and reconnect the event in case we have
        # to set it to active and we don't want the signal to be processed
        if not widget.get_active():
            widget.disconnect(widget.signal_id)
            widget.set_active(True)
            widget.signal_id = widget.connect('activate', self.open)

        self.db.add(widget.item_id)
        webbrowser.open(widget.url)

        if self.commentState:

            webbrowser.open(widget.discussion_url)

    def add_item(self, item):
        """Adds an item to the menu"""

        i = gtk.CheckMenuItem(
            "(" + str(item['votes_count']).zfill(3) + "/" + str(item['comments_count']).zfill(3) + ")    " +
            item['name'] + ' >> ' + item['tagline'])

        visited = item['history'] or item['id'] in self.db

        i.set_active(visited)
        i.url = item['redirect_url']
        maker = 'N/A'
        if len(item['makers']) > 0:
            maker = item['makers'][0]['name']

        tooltip = "{url}\nPosted by {user} {timeago}".format(url=item['redirect_url'],
                                                             user=maker,
                                                             timeago=item['day'])
        i.set_tooltip_text(tooltip)
        i.signal_id = i.connect('activate', self.open)
        i.hn_id = item['id']
        i.item_id = item['id']
        i.discussion_url = item['discussion_url']
        self.menu.prepend(i)
        i.show()

    def refresh(self, widget=None, no_timer=False, chrome_data_directory=None, firefox_data_directory=None):

        """Refreshes the menu """
        try:
            # Create an array of 20 false to denote matches in History
            searchResults = [False] * 20
            data = list(reversed(ProductHunt.getHomePage()[0:20]))
            urls = [item['redirect_url'] for item in data]
            if chrome_data_directory:
                searchResults = self.merge_bool_array(searchResults, Chrome.search(urls, chrome_data_directory))

            if firefox_data_directory:
                searchResults = self.merge_bool_array(searchResults, Firefox.search(urls, firefox_data_directory))

            # Remove all the current stories
            for i in self.menu.get_children():
                if hasattr(i, 'url'):
                    self.menu.remove(i)

            # Add back all the refreshed news
            for index, item in enumerate(data):
                item['history'] = searchResults[index]

                self.add_item(item)
        # Catch network errors
        except requests.exceptions.RequestException as e:
            print("[+] There was an error in fetching news items")
        finally:
            # Call every 10 minutes
            if not no_timer:
                gtk.timeout_add(10 * 30 * 1000, self.refresh, widget, no_timer, chrome_data_directory)

    # Merges two boolean arrays, using OR operation against each pair
    def merge_bool_array(self, original, patch):
        for index, var in enumerate(original):
            original[index] = original[index] or patch[index]
        return original


def main():
    parser = argparse.ArgumentParser(description='ProductHunt in your System Tray')
    parser.add_argument('-v', '--version', action='version', version='0.0.1')
    parser.add_argument('-c', '--comments', dest='comments', action='store_true',
                        help="Load the PH comments link for the product as well")
    parser.add_argument('--chrome', dest='chrome',
                        help="Specify a Google Chrome Profile directory to use for matching chrome history")
    parser.add_argument('--firefox', dest='firefox',
                        help="Specify a Firefox Profile directory to use for matching firefox history")
    parser.set_defaults(comments=False)
    args = parser.parse_args()
    indicator = HunterTrayApp(args)
    indicator.run()


if __name__ == '__main__':
    main()
