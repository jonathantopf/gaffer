##########################################################################
#  
#  Copyright (c) 2011, John Haddon. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

from PySide import QtCore

import Gaffer
import GafferUI

class Dialogue( GafferUI.Window ) :

	def __init__( self, title ) :
	
		GafferUI.Window.__init__( self, title, borderWidth = 8 )
		
		self._qtWidget().setWindowFlags( QtCore.Qt.WindowFlags( QtCore.Qt.Dialog ) )
		
		self.__column = GafferUI.ListContainer( GafferUI.ListContainer.Orientation.Vertical, spacing = 8 )
		
		self.__column.append( GafferUI.Frame(), True )
		
		self.__buttonRow = GafferUI.ListContainer( GafferUI.ListContainer.Orientation.Horizontal, spacing=8 )
		self.__column.append( self.__buttonRow )
		
		self.setChild( self.__column )
			
	def waitForButton( self ) :
	
		assert( len( self.__buttonRow ) )
	
		self.setVisible( False )
		self._qtWidget().setWindowModality( QtCore.Qt.ApplicationModal )
		self.setVisible( True )
				
		self.__buttonConnections = []
		self.__closeConnection = self.closeSignal().connect( self.__close )
		for button in self.__buttonRow :
			self.__buttonConnections.append( button.clickedSignal().connect( self.__buttonClicked ) )
		
		self.__resultOfWait = None
		GafferUI.EventLoop.start() # returns when a button has been pressed
		self.__buttonConnections = []
		self.__closeConnection = None

		self._qtWidget().setWindowModality( QtCore.Qt.NonModal )
						
		return self.__resultOfWait
		
	def _setWidget( self, widget ) :
	
		self.__column[0] = widget
		
	def _getWidget( self ) :
		
		return self.__column[0]
		
	def _addButton( self, label ) :
		
		button = GafferUI.Button( label=label )
		self.__buttonRow.append( button )		
		return button
		
	def __buttonClicked( self, button ) :
	
		# check we're in a call to _waitForButton
		assert( len( self.__buttonConnections ) )
		
		self.__resultOfWait = button
		GafferUI.EventLoop.stop()
		
	def __close( self, widget ) :
	
		# check we're in a call to _waitForButton
		assert( len( self.__buttonConnections ) )

		self.__resultOfWait = None
		GafferUI.EventLoop.stop()