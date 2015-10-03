#Changelog

# v.0.1 #

initial release


# v.0.2 #

  * major speed improvements of server status requests (makes server search up to two times faster than in v.0.1. Refresh of favorites and recent servers are faster, too)
  * new feature: buddylist. Search servers based on the names of players playing on them. (note: search is case sensitiv!) Manage (add/remove) your Buddies and look where they are playing.
  * serverlists are now sortable by clicking on the table headers
  * added option to set a default tab in the settings
  * fixed bug that prevented a server to be removed from the recent serverslist
  * progressbar issues fixed
  * password of servers can now be remembered. There now is also a checkbox in the password dialog that can enable/disable this function.
  * fixed a bug that causes servers to appear multiple times in the serverlist after multiple searches
  * a lock-icon is now displayed for passworded servers instead of the string 'yes'
  * the selected row in a serverlist is now updated too, if the refresh-button in the details area is clicked.
  * plus some minor bugfixes


# v.0.2.1 #

  * spelling of some labels
  * added 'Add to Favorites' button to the serverdetails area on the 'Buddies' tab


# v.0.3 #

  * added option to disable the update of the selected server row when refresh button is clicked
  * remember filter/query parameters
  * some "under the hood" code improvements
  * fixed a bug that prevented the lock-icon to be displayed on the "Recently Played" tab
  * added feature to display location of the server as a small flag icon
  * handle players with blank names as UnnamedPlayer
  * applied patch to make UrTSB work on windows (contributed by Courgette from the urbanterror.info forums)
  * server connect on double-click / enter pressed and F5 key refreshes serverdetails
  * playerlist and server var list are now sortable
  * now launching UrT in a subprocess ( to avoid that UrTSB is blocked while UrT is running)
  * new feature: RCON window for remote server administration
  * added contextmenus to the serverlist and the playerlist

# v.0.4 #

  * applied patch to make UrTSB work on windows (contributed by Courgette from the urbanterror.info forums) + some more changes needed to provide a windows version of UrTSB
  * make use of python distutils (UrTSB can now be installed by calling "_python setup.py install_")
  * adding a server manually to the favorites now handles the host to be specified by url and not only by ip
  * added logo/icon
  * new filtering panel - advanced filter. The old basic filter panel remains the default. The new advanced filter panel can be activated in the settings. Features:
> - more filter options: g\_gear (incl. g\_gear calculator), custom variable filtering, servername and mapnamefilter.

> - Refresh of the Serverlist without new master server query

> - Direct server lookup by ip:port or url:port
  * added abort button to abort a query/search/refresh.
  * display servername on rcon window
  * two new context menuitems: "copy address to clipboard" and "copy name and address to clipboard"
  * added commandline option -d (or --debug) which activates debug output
  * added status icons to buddylist (online/offline)
  * removed update selected row on refresh
  * added option to start a buddysearch on startup if the buddytab is set as the default tab
  * window now remembers size and position

# v.0.5 #

**not yet released - in development**

  * display private slots ([issue #1](https://code.google.com/p/urtsb/issues/detail?id=#1))
  * fixed server sorting by playercount ([issue #3](https://code.google.com/p/urtsb/issues/detail?id=#3))