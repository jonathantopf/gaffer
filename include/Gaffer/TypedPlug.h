//////////////////////////////////////////////////////////////////////////
//  
//  Copyright (c) 2011, John Haddon. All rights reserved.
//  
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//  
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//  
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//  
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//  
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  
//////////////////////////////////////////////////////////////////////////

#ifndef GAFFER_TYPEDPLUG_H
#define GAFFER_TYPEDPLUG_H

#include "OpenEXR/ImathMatrix.h"

#include "Gaffer/ValuePlug.h"

namespace Gaffer
{

template<typename T>
class TypedPlug : public ValuePlug
{

	public :

		typedef T ValueType;

		IECORE_RUNTIMETYPED_DECLARETEMPLATE( TypedPlug<T>, ValuePlug );

		TypedPlug(
			const std::string &name = staticTypeName(),
			Direction direction=In,
			const T &defaultValue = T(),
			unsigned flags = None
		);
		virtual ~TypedPlug();

		/// Accepts only instances of TypedPlug<T> or derived classes.
		virtual bool acceptsInput( ConstPlugPtr input ) const;

		const T &defaultValue() const;

		/// \undoable
		void setValue( const T &value );
		/// Returns the value. This isn't const as it may require a compute
		/// and therefore a setValue().
		const T &getValue();

	protected :

		virtual void setFromInput();

	private :

		IE_CORE_DECLARERUNTIMETYPEDDESCRIPTION( TypedPlug<T> );		

		void setValueInternal( T value );
	
		T m_value;
		T m_defaultValue;

};

typedef TypedPlug<std::string> StringPlug;
typedef TypedPlug<Imath::M33f> M33fPlug;
typedef TypedPlug<Imath::M44f> M44fPlug;

IE_CORE_DECLAREPTR( StringPlug );
IE_CORE_DECLAREPTR( M33fPlug );
IE_CORE_DECLAREPTR( M44fPlug );

} // namespace Gaffer

#endif // GAFFER_TYPEDPLUG_H