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

import inspect
import weakref

from PySide import QtCore
from PySide import QtGui

from IECore import curry

import GafferUI
import CamelCase

class Menu( GafferUI.Widget ) :

	def __init__( self, definition, _qtMenu=None ) :
	
		GafferUI.Widget.__init__( self, _qtMenu if _qtMenu else QtGui.QMenu() )
	
		self.definition = definition
		
		self._qtWidget().connect( self._qtWidget(), QtCore.SIGNAL( "aboutToShow()" ), self.__show )
		
		self.__popupParent = None
		
	## Displays the menu at the current pointer position, and attached to
	# an optional parent.
	def popup( self, parent=None ) :
	
		if parent is not None :
			self.__popupParent = weakref.ref( parent )
		else :
			self.__popupParent = None
			
		self._qtWidget().popup( QtGui.QCursor.pos() )

	## Reimplemented from Widget to report the parent passed to popup().
	def parent( self ) :
	
		if self.__popupParent is not None :
			p = self.__popupParent()
			if p is not None :
				return p
			
		return GafferUI.Widget.parent( self )
		
	def __commandWrapper( self, command, toggled ) :
	
		args = []
		kw = {}
		commandArgs = inspect.getargspec( command )[0]

		if "menu" in commandArgs :
			kw["menu"] = self
		
		if "checkBox" in commandArgs :
			kw["checkBox"] = toggled
		#elif qtAction.isCheckable() :
			# workaround for the fact that curried functions
			# don't have arguments we can query right now. we
			# just assume that if it's a check menu item then
			# there must be an argument to receive the check
			# status.
		#	args.append( toggled )
		
		command( *args, **kw )

	def __show( self ) :
		
		definition = self.definition		
		if callable( definition ) :
			definition = definition()
			
		self._qtWidget().clear()
			
		done = set()
		for path, item in definition.items() :
		
			pathComponents = path.strip( "/" ).split( "/" )
			name = pathComponents[0]
						
			if not name in done :

				menuItem = None
				if len( pathComponents ) > 1 :
					
					# it's a submenu
					pass
					#subMenu = gtk.Menu()
					#subMenuDefinition = definition.reRooted( "/" + name + "/" )
					#subMenu.connect( "show", Menu.__show, subMenuDefinition )

					#menuItem = gtk.MenuItem( label = name )
					#menuItem.set_submenu( subMenu )
						
				else :
				
					# it's not a submenu
					
					if item.divider :
						
						self._qtWidget().addSeparator()
						
					elif item.subMenu :
					
						pass
						#subMenu = gtk.Menu()
						#subMenu.connect( "show", Menu.__show, item.subMenu )
						#menuItem = gtk.MenuItem( label = name )
						#menuItem.set_submenu( subMenu )						
											
					else :
					
						qtAction = QtGui.QAction( name, self._qtWidget() )
						
						if item.checkBox :
							qtAction.setCheckable( item.checkBox() )
						
						active = False
						if item.command :
						
							active = item.active
							if callable( active ) :
								active = active()
							
							## \todo Check we're not making unbreakable circular references here
							if item.checkBox :	
								qtAction.connect( qtAction, QtCore.SIGNAL( "toggled( bool )" ), curry( self.__commandWrapper, item.command ) )							
							else :
								qtAction.connect( qtAction, QtCore.SIGNAL( "triggered( bool )" ), curry( self.__commandWrapper, item.command ) )
												
						qtAction.setEnabled( active )
	
						self._qtWidget().addAction( qtAction )
						
				done.add( name )
