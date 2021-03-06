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


from favoritesfilter import FavoritesFilter
from statusbar import StatusBar
from urtsb_src.filemanager import FileManager, cfgkey
from urtsb_src.guicontroller import GuiController
from urtsb_src.ui.basetab import BaseTab
from urtsb_src.ui.passworddialog import PasswordDialog, PassDialogType
from urtsb_src.ui.playerlist import PlayerList
from urtsb_src.ui.serverdetailbox import ServerDetailBox
from urtsb_src.ui.serverlist import ServerList
import gtk






class FavoritesTab(BaseTab):
    """
    UI Element for the content of the favorites tab.
    """
    


    def __init__(self):
        """
        Constructor
        """
        gtk.VBox.__init__(self)
        
        self.filter = FavoritesFilter()
        self.filter.show()
        
        self.pack_start(self.filter, False, False)
        
       
        # top pane area 
        paned = gtk.VPaned() 
        paned.show()
        self.pack_start(paned)   
        
        
        # bottom add a statusbar
        self.statusbar = StatusBar(self)
        self.pack_start(self.statusbar, False, False)
        
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
        
        
        refresh_button = gtk.Button('Refresh')
        refreshimage = gtk.Image()
        refreshimage.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_BUTTON)
        refresh_button.set_image(refreshimage)
        
        connect_button = gtk.Button('Connect')
        connectimage = gtk.Image()
        connectimage.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)
        connect_button.set_image(connectimage)
        
        removefav_button = gtk.Button('Remove from Favorites')
        removeimage = gtk.Image()
        removeimage.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_BUTTON)
        removefav_button.set_image(removeimage)
        
        
        buttonbox.pack_start(refresh_button, True, True)
        buttonbox.pack_start(connect_button, True, True)
        buttonbox.pack_start(removefav_button, False, False)
        refresh_button.connect("clicked", self.onRefreshButtonClicked)
        removefav_button.connect("clicked", self.onRemoveFavoriteClicked)
        connect_button.connect("clicked", self.connect_button_clicked)
        
        self.show_all()
        
        # self.pack_start(button,False)
    def connect_button_clicked(self, widget):
        """
        Callback of the the connect button
        """
        
        gui = GuiController()
        server = self.detailsbox.current_server
        if server:
            if server.needsPassword():
                passdialog = PasswordDialog(server, PassDialogType\
                                                               .SERVER_PASSWORD)
                passdialog.run()
            else:
                gui.connectToServer(server)
                
    def onRemoveFavoriteClicked(self, widget):
        """
        Callback method for the remove button. Triggers the removal of 
        the favorite entry by calling the gui controller which then 
        removes the favorite (from list in memory and also from file)
        Also removes the favorite directly from the liststore.
        
        @param widget - the widget that emitted the clicked signal - the button 
        """
        
        #the current selected server displayed in the details
        server = self.detailsbox.current_server
        if server: 
            #remove it from the favoriteslist
            gui = GuiController()
            gui.removeFavorite(server)
            
            #remove row from liststore
            selection = self.serverlist.serverlistview.get_selection()
            result = selection.get_selected()
            if result: 
                model, iter = result
                model.remove(iter)
            
       
    def onRefreshButtonClicked(self, widget):
        """
        Callback of the refreshbutton.
        """
        
        selection = self.serverlist.serverlistview.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            row =  model[paths[0][0]]
            server = row[8]
            guicontroller = GuiController()
            guicontroller.setDetailServer(server, self)
            
            
    def addServer(self, server):
        """
        Add a server to the listview/store.
        Called by the guicontroller.
        """
        self.serverlist.addServer(server)
    
    def clearServerList(self):
        """
        Clears the embeded serverlist treeview
        """
        self.serverlist.clear()
   
    def setServerdetails(self, server):
        """
        Updates the embedded serverdetails element 
        """
        self.playerlist.clear()
        
        for player in server.getPlayerList():
            self.playerlist.addPlayer(player)
            
        self.detailsbox.setServerDetails(server) 
        # update row in list
        # but only if the corresponding option is True
        fm = FileManager()
        config = fm.getConfiguration()
        if 'True' == config[cfgkey.OPT_UPDATE_SL_ROW]: 
            self.serverlist.update_selected_row(server)
       
    def serverlist_loading_finished(self):
        """
        Callback method executed when the search has finished
        """
        #reactivate the search button
        self.filter.refresh_button.set_sensitive(True)    
        self.statusbar.lock()
        self.qm = None         
