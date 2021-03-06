#
# Copyright (C) 2010  Sorcerer
#
# This file is part of UrTSB.
#
# UrTSB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UrTSB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UrTSB.  If not, see <http://www.gnu.org/licenses/>.
#



from urtsb_src.globals import Globals
from urtsb_src.guicontroller import GuiController
from urtsb_src.ui.addbuddydialog import AddBuddyDialog
from urtsb_src.ui.basetab import BaseTab
from urtsb_src.ui.buddiesfilter import BuddiesFilter
from urtsb_src.ui.playerlist import PlayerList
from urtsb_src.ui.serverdetailbox import ServerDetailBox
from urtsb_src.ui.serverlist import ServerList
from urtsb_src.ui.statusbar import StatusBar
import gtk





class BuddiesTab(BaseTab):
    """
    This is the gui tab for the buddylist feature
    """


    def __init__(self):
        """
        Constructor
        """
        
        gtk.VBox.__init__(self)
        
        #prepare images:
        offline_image = gtk.Image()
        offline_image.set_from_file(Globals.icon_dir+'/gray-icon.png')
        self.offline_pixbuf = offline_image.get_pixbuf()
        
        online_image = gtk.Image()
        online_image.set_from_file(Globals.icon_dir+'/green-icon.png')
        self.online_pixbuf = online_image.get_pixbuf()
        
        
        mainbox = gtk.HBox()
        
        self.pack_start(mainbox)
        
        
        buddieslistview = self.create_buddy_list_view()
        mainbox.pack_start(buddieslistview, False, False)
        
        
        serverlistbox = gtk.VBox()
        mainbox.pack_start(serverlistbox)
        
        self.filter = BuddiesFilter(self)
        self.filter.show()
        
        serverlistbox.pack_start(self.filter, False, False)
        
        # top pane area 
        paned = gtk.VPaned() 
        paned.show()
        serverlistbox.pack_start(paned)   
        
        
        # bottom add a statusbar
        self.statusbar = StatusBar(self)
        serverlistbox.pack_start(self.statusbar, False, False)
        
        # serverlist window
        self.serverlist = ServerList(self)
        paned.pack1(self.serverlist, True, False)
        #paned.add1(self.serverlist)
        
        
        # bottom panearea
        bottompane = gtk.HPaned()
        paned.pack2(bottompane, True, False)
        #paned.add2(bottompane)
        
        #left box
        self.playerlist = PlayerList()
        bottompane.pack1(self.playerlist, False, False)
        
        
        
        #right box
        self.detailsbox = ServerDetailBox()
        vbox = gtk.VBox()
        
        
        bottompane.pack2(vbox, True, False)
        
      
        buttonbox = gtk.HBox()
        #self.detailsbox.pack_start(buttonbox, False, False)
        vbox.pack_start(buttonbox, False, False)
        vbox.pack_start(self.detailsbox)
        
        addfav_button = gtk.Button('Add to Favorites')
        favimage = gtk.Image()
        favimage.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON)
        addfav_button.set_image(favimage)
        
        
        refresh_button = gtk.Button('Refresh')
        refreshimage = gtk.Image()
        refreshimage.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_BUTTON)
        refresh_button.set_image(refreshimage)
        
        connect_button = gtk.Button('Connect')
        connectimage = gtk.Image()
        connectimage.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)
        connect_button.set_image(connectimage)
        
        
        buttonbox.pack_start(refresh_button, True, True)
        buttonbox.pack_start(connect_button, True, True)
        buttonbox.pack_start(addfav_button, True, True)
        
        refresh_button.connect("clicked", self.onRefreshButtonClicked)
        addfav_button.connect("clicked", self.onAddFavButtonClicked)
        connect_button.connect("clicked", self.connect_button_clicked)
        
        self.show_all()
      
            
    def create_buddy_list_view(self):
        """
        Builds the gui elements for the buddylist
        """
        
        buddybox = gtk.VBox()
                
        scrolled_window = gtk.ScrolledWindow()
        buddybox.pack_start(scrolled_window)
        self.buddyliststore = gtk.ListStore(gtk.gdk.Pixbuf, str)
        

        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        
        self.buddylistview = gtk.TreeView(model=self.buddyliststore)
        self.buddylistview.show()
        self.buddylistview.set_headers_clickable(True)
        scrolled_window.add(self.buddylistview)
        
       
        
        column_status = gtk.TreeViewColumn('')
        self.buddylistview.append_column(column_status)
        
        column_buddyname = gtk.TreeViewColumn('Buddy')
        self.buddylistview.append_column(column_buddyname)
        
        column_buddyname.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        
        column_buddyname.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_buddyname.set_expand(True)
        column_buddyname.set_fixed_width(100)
        
        
        player_cell0=gtk.CellRendererText()
        status_cell1=gtk.CellRendererPixbuf()
        
        column_buddyname.pack_start(player_cell0, expand=True)
        column_status.pack_start(status_cell1, expand=False)
        
        column_buddyname.add_attribute(player_cell0, 'text', 1)
        column_status.add_attribute(status_cell1, 'pixbuf', 0)
        
        buttonbox = gtk.HBox()
        buddybox.pack_start(buttonbox, False, False)
        add_button = gtk.Button('Add Buddy')
        add_button.connect("clicked", self.on_add_buddy_clicked)
        add_button.set_border_width(5)
        
        remove_button = gtk.Button('Remove Selected')
        remove_button.connect("clicked", self.on_remove_buddy_clicked)
        remove_button.set_border_width(5)
        
        buttonbox.pack_start(add_button, True, True)
        buttonbox.pack_start(remove_button, True, True)
        
        buddybox.show_all()
        
        return buddybox
    
    def on_add_buddy_clicked(self, button):
        """
        Callback for the add buddy button. Opens the dialog
        to add a buddy
        """
        add_dialog = AddBuddyDialog(self)
        add_dialog.run()
        
    def clear_buddy_list(self):
        """
        Clears the buddylist
        """
        self.buddyliststore.clear()
        
    def append_buddy_to_list(self, buddyname):
        """
        Appends an entry to the buddylist treeview/liststore
        
        @param buddyname name of the biddy to be added to the liststore
        """
        self.buddyliststore.append([self.offline_pixbuf, buddyname])
        
    def on_remove_buddy_clicked(self, widget):
        """
        Callback for the remove buddy button
        """
        selection = self.buddylistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            name_to_remove = self.buddyliststore.get_value(iter, 1)
            gc = GuiController()
            gc.remove_buddy(name_to_remove)
            self.buddyliststore.remove(iter)
  
    def update_buddy_status(self, name, status):
        """
        Updates the status image in the buddylist
        
        @param the name to be updated
        @param status - True = online, False = offline
        """
        iter = self.buddyliststore.iter_children(None)
        while iter:
            value = self.buddyliststore.get_value(iter, 1)
            if value == name:
                if status:
                    self.buddyliststore.set_value(iter, 0, self.online_pixbuf)
                else:
                    self.buddyliststore.set_value(iter, 0, self.offline_pixbuf)
            iter = self.buddyliststore.iter_next(iter)
            
    def set_all_buddies_to_offline(self):
        """
        Sets the status image of all entries in the buddylist to offline.
        Done right before a new search is started.
        """
        iter = self.buddyliststore.iter_children(None)
        while iter:
            self.buddyliststore.set_value(iter, 0, self.offline_pixbuf)
            iter = self.buddyliststore.iter_next(iter)
        
    def serverlist_loading_finished(self):
        """
        Callback method executed when the search has finished
        """
        #reactivate the search button
        self.filter.search_button.set_sensitive(True)
        self.filter.playersearchbutton.set_sensitive(True) 
        self.statusbar.lock()
        self.qm = None
    
