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

import math

from PySide import QtCore
from PySide import QtGui

import Gaffer
import GafferUI

class Slider( GafferUI.Widget ) :

	def __init__( self, position = 0.5 ) :
	
		GafferUI.Widget.__init__( self, QtGui.QWidget() )
		
		self._qtWidget().setSizePolicy( QtGui.QSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum ) )
		self._qtWidget().setMinimumSize( 18, 18 )
		
		self.__position = position

		self.__buttonPressConnection = self.buttonPressSignal().connect( self.__buttonPress )
		self.__mouseMoveConnection = self.mouseMoveSignal().connect( self.__mouseMove )

		self._qtWidget().paintEvent = Gaffer.WeakMethod( self.__paintEvent )
		
	def setPosition( self, p ) :
				
		if p!=self.__position :
		
			self.__position = p
			self._qtWidget().update()
			
			try :
				signal = self.__positionChangedSignal
			except :
				return
			
			signal( self )
			
	def getPosition( self ) :
	
		return self.__position	
	
	def positionChangedSignal( self ) :
	
		try :
			return self.__positionChangedSignal
		except :
			self.__positionChangedSignal = GafferUI.WidgetSignal()
			
		return self.__positionChangedSignal
	
	## \todo Colours should come from some unified style somewhere
	def _drawBackground( self, painter ) :
	
		size = self.size()

		pen = QtGui.QPen( QtGui.QColor( 0, 0, 0 ) )
		pen.setWidth( 1 )
		painter.setPen( pen )
		
		painter.drawLine( 0, size.y / 2, size.x, size.y / 2 )
		
	def _drawPosition( self, painter ) :
	
		size = self.size()

		pen = QtGui.QPen( QtGui.QColor( 0, 0, 0 ) )
		pen.setWidth( 1 )
		painter.setPen( pen )
		
		brush = QtGui.QBrush( QtGui.QColor( 128, 128, 128 ) )
		painter.setBrush( brush )
		
		painter.drawEllipse( QtCore.QPoint( self.__position * size.x, size.y / 2 ), size.y / 4, size.y / 4 )
		
	def __paintEvent( self, event ) :
	
		painter = QtGui.QPainter( self._qtWidget() )
		painter.setRenderHint( QtGui.QPainter.Antialiasing )
		
		self._drawBackground( painter )
		self._drawPosition( painter )
			
	def __buttonPress( self, gtkWidget, event ) :
	
		if event.buttons & GafferUI.ButtonEvent.Buttons.Left :
			self.setPosition( float( event.line.p0.x ) / self.size().x )

	def __mouseMove( self, gtkWidget, event ) :
	
		if event.buttons & GafferUI.ButtonEvent.Buttons.Left :
			self.setPosition( float( event.line.p0.x ) / self.size().x )
