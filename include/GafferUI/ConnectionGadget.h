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

#ifndef GAFFERUI_CONNECTIONGADGET_H
#define GAFFERUI_CONNECTIONGADGET_H

#include "GafferUI/Gadget.h"

#include "Gaffer/Plug.h"

namespace GafferUI
{
	IE_CORE_FORWARDDECLARE( Nodule )
}

namespace GafferUI
{

class ConnectionGadget : public Gadget
{

	public :

		ConnectionGadget( GafferUI::NodulePtr srcNodule, GafferUI::NodulePtr dstNodule );
		virtual ~ConnectionGadget();

		IE_CORE_DECLARERUNTIMETYPEDEXTENSION( ConnectionGadget, ConnectionGadgetTypeId, Gadget );
		
		/// Accepts only GraphGadgets as parent.
		virtual bool acceptsParent( const Gaffer::GraphComponent *potentialParent ) const;		
		virtual Imath::Box3f bound() const;
		
		NodulePtr srcNodule();
		NodulePtr dstNodule();
		
	protected :

		void setSrcPos( const Imath::V3f &p );
		void setDstPos( const Imath::V3f &p );
		void setPositionsFromNodules();
		
		void doRender( IECore::RendererPtr renderer ) const;

	private :
		
		bool buttonPress( GadgetPtr gadget, const ButtonEvent &event );
		IECore::RunTimeTypedPtr dragBegin( GadgetPtr gadget, const DragDropEvent &event );	
		bool dragUpdate( GadgetPtr gadget, const DragDropEvent &event );
		bool dragEnd( GadgetPtr gadget, const DragDropEvent &event );
		
		Imath::V3f m_srcPos;
		Imath::V3f m_dstPos;
		
		NodulePtr m_srcNodule;
		NodulePtr m_dstNodule;
		
		Gaffer::Plug::Direction m_dragEnd;
		
};

IE_CORE_DECLAREPTR( ConnectionGadget );

} // namespace GafferUI

#endif // GAFFERUI_CONNECTIONGADGET_H