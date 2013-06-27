using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;

namespace SpringCat.NET.Network.TCP
{
	public class AsyncResultConnect : AsyncResult
	{
		private IOEngine engine_;

		public AsyncResultConnect(Socket handle, IOEngine engine)
			: base(handle)
		{
			engine_ = engine;
		}

		public override void Process(uint numberOfBytesTransferred)
		{
			Link link = new Link(Handle, engine_);
			link.OnLinkOpened();
		}
	}
}
