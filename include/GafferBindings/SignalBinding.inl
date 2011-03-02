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

#ifndef GAFFERBINDINGS_SIGNALBINDING_INL
#define GAFFERBINDINGS_SIGNALBINDING_INL

#include "GafferBindings/ConnectionBinding.h"

namespace GafferBindings
{

template<int Arity, typename Signal>
struct DefaultSignalCallerBase;

template<typename Signal>
struct DefaultSignalCallerBase<1, Signal>
{
	static typename Signal::result_type call( Signal &s, typename Signal::arg1_type a1 )
	{
		return s( a1 );
	}
};

template<typename Signal>
struct DefaultSignalCallerBase<2, Signal>
{
	static typename Signal::result_type call( Signal &s, typename Signal::arg1_type a1, typename Signal::arg2_type a2 )
	{
		return s( a1, a2 );
	}
};

template<typename Signal>
struct DefaultSignalCallerBase<3, Signal>
{
	static typename Signal::result_type call( Signal &s, typename Signal::arg1_type a1, typename Signal::arg2_type a2, typename Signal::arg3_type a3 )
	{
		return s( a1, a2, a3 );
	}
};

template<typename Signal>
struct DefaultSignalCaller : public DefaultSignalCallerBase<Signal::slot_function_type::arity, Signal>
{

};

template<typename Signal, typename SignalCaller, typename SlotCaller>
void SignalBinder<Signal, SignalCaller, SlotCaller>::bind( const char *className )
{

	boost::python::class_<Signal, boost::noncopyable>( className )
		.def( "connect", &Connection::create<Signal, SlotCaller> )
		.def( "__call__", &SignalCaller::call )
	;

}

} // namespace GafferBindings

#endif // GAFFERBINDINGS_SIGNALBINDING_INL