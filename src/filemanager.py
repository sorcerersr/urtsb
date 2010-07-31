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

from server import Server
import os

class FileManager(object):
    """
    This class handles all file accesses of UrTSB.
    
    1. read/write of configuration
    2. access file for loading/storing favorites list
    3. access file for loading/storing recent servers
    
    """
    __shared_state = {} # borg pattern
    
    instance = None

    favorites = None
    recentservers = None
    
    #filenames
    conf_file = 'urtsb.cfg'
    fav_file = 'favorites.srv'
    rec_file = 'recent.srv'

    def __init__(self):
        """
        Constructor
        """
        self.__dict__ = self.__shared_state # borg pattern
        
        if not self.instance:
            self.instance = True
            
            # linux specific! if someday UrTSB should run on another OS
            # this definitely needs to be extended
            self.configfolder = os.environ['HOME']+'/.urtsb/' 
            if not os.path.exists(self.configfolder):
                try:
                    os.makedirs(self.configfolder)
                except OSError:
                    pass
            # extend filenames with path to the configurationfolder
            self.fav_file = self.configfolder+self.fav_file
            self.rec_file = self.configfolder+self.rec_file
            self.conf_file = self.configfolder+self.conf_file
           
    
    def getFavorites(self):
        """
        Get the Favorites. If already loaded from file, return the instance from
        memory, otherwise load from file. 
        
        @return dict of server objects (key = adress)
        """
        if self.favorites:
            return self.favorites
        
        self.favorites = {}
        fobj = None
        try:
            fobj = open(self.fav_file, "r") 
        except IOError:
            #the file does not exist! just return the empty dict created earlier
            return self.favorites
        
        for line in fobj: 
            line = line.strip() 
            serverinfo = line.split(',') # file is a csv
            #format: ip,port,password,servername
            server = Server(serverinfo[0], int(serverinfo[1]))
            server.setPassword(serverinfo[2])
            server.setName(serverinfo[3])
            #use the adress (ip:port) as key to avoid duplicate entries
            self.favorites[server.getAdress()] = server
        fobj.close()
        
        return self.favorites
    
    def addFavorite(self, server):
        """
        Adds a new favorite server to the list of favorites.
        Note: Immediately writes the current state of the list 
        into the favorites file. 
        
        @param server - the server object to add
        """
        favs = self.getFavorites() # this makes sure it is initialized 
        if server.getAdress() not in favs:
            self.favorites[server.getAdress()] = server
            #immdediately save to file in order to avoid a loss of data (crash etc.)
            self.saveFavorites()
    
    def removeFavorite(self, server):
        """
        Removes a existing favorite server from the favorites list.
        Note: Immediately updates the favorties file.
        
        @param server - the server object to be removed
        """
        favs = self.getFavorites() # this makes sure it is initialized  
        if server.getAdress() in favs:
            del self.favorites[server.getAdress()]
            self.saveFavorites()
    
    def addRecent(self, server):
        """
        Adds a new server to the list of recent connected servers.
        Note: Immediately writes the current state of the list 
        into the recent servers file. 
        
        @param server - the server object to add
        """
        if server.getAdress() not in self.recentservers:
            self.recentservers[server.getAdress()] = server
            #immdediately save to file in order to avoid a loss of data (crash etc.)
            self.saveRecentServers()
            
    def saveFavorites(self):
        """
        Performs the writing to the favorites file.
        """
        fobj = open(self.fav_file, "w") 
        for key in self.favorites:
            server = self.favorites[key]
            #format: ip,port,password,servername
            fobj.write(server.getHost() + ',' + str(server.getPort()) 
                       + ',' + server.getPassword() + ',' + server.getName() + '\n')
        fobj.close()
        
    def saveRecentServers(self):
        """
        Performs the writing to the recent servers file
        """
        fobj = open(self.rec_file, "w") 
        for server in self.recentservers:
            #format: ip,port,password, connectioncount,dateoflastconnection,name
            fobj.write(server.getHost() + ',' + str(server.getPort()) 
                     + ',' + server.getPassword() + ',' + server.getConnections() + ','
                     + server.getLastConnect() + ',' + server.getName() + '\n')
        fobj.close()
    
    def getRecentServers(self):
        """
        Get the Recent Servers. If already loaded from file, return the instance from
        memory, otherwise load from file. 
        
        @return dict of server objects (key = adress)
        """
        if self.recentservers:
            return self.recentservers
        
        self.recentservers = {}
        fobj = None
        try:
            fobj = open(self.rec_file, "r") 
        except IOError:
            #the file does not exist! just return the empty dict created earlier
            return self.recentservers
        
        for line in fobj: 
            line = line.strip() 
            serverinfo = line.split(',') # file is a csv
            #format: ip,port,password, connectioncount,dateoflastconnection,name
            server = Server(serverinfo[0], serverinfo[1])
            server.setPassword(serverinfo[2])
            server.setConnections(serverinfo[3])
            server.setLastConnect(serverinfo[4])
            server.setName(serverinfo[5])
            self.recentservers[server.getAdress()] = server
        fobj.close()
        
        return self.recentservers        