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

import unittest

import IECore

import Gaffer

class NumericPlugTest( unittest.TestCase ) :

	def testConstructor( self ) :
	
		f = Gaffer.FloatPlug()
		self.assertEqual( f.defaultValue(), 0 )
		self.assertEqual( f.getName(), "FloatPlug" )
		
		f = Gaffer.FloatPlug( direction=Gaffer.Plug.Direction.Out, defaultValue = 1,
			minValue = -1, maxValue = 10 )
			
		self.assertEqual( f.direction(), Gaffer.Plug.Direction.Out )
		self.assertEqual( f.defaultValue(), 1 )
		self.assertEqual( f.minValue(), -1 )
		self.assertEqual( f.maxValue(), 10 )
		
		f = Gaffer.FloatPlug( defaultValue=10, name="a" )
		self.assertEqual( f.defaultValue(), 10 )
		self.assertEqual( f.getName(), "a" )
		self.assertEqual( f.typeName(), "FloatPlug" )
	
	def testHaveMinMaxValues( self ) :
	
		f = Gaffer.FloatPlug()
		self.assertEqual( f.hasMinValue(), False )
		self.assertEqual( f.hasMaxValue(), False )
		
		f = Gaffer.FloatPlug( minValue=1 )
		self.assertEqual( f.hasMinValue(), True )
		self.assertEqual( f.hasMaxValue(), False )
		
		f = Gaffer.FloatPlug( maxValue=1 )
		self.assertEqual( f.hasMinValue(), False )
		self.assertEqual( f.hasMaxValue(), True )
	
	def testConstructWithInputOrValue( self ) :
	
		f1 = Gaffer.FloatPlug()
		
		f2 = Gaffer.FloatPlug( input=f1 )
		self.assert_( f2.getInput().isSame( f1 ) )
		
		f1 = Gaffer.FloatPlug( value=10 )
		self.assertEqual( f1.getValue(), 10 )
		
		self.assertRaises( ValueError, Gaffer.FloatPlug, input=f1, value=10 )
		
	def testRunTimeTyping( self ) :
	
		f = Gaffer.FloatPlug()
		i = Gaffer.IntPlug()
		
		self.assert_( f.isInstanceOf( Gaffer.FloatPlug.staticTypeId() ) )			
		self.assert_( not f.isInstanceOf( Gaffer.IntPlug.staticTypeId() ) )			
		self.assert_( not i.isInstanceOf( Gaffer.FloatPlug.staticTypeId() ) )			
		self.assert_( i.isInstanceOf( Gaffer.IntPlug.staticTypeId() ) )			

if __name__ == "__main__":
	unittest.main()
	