using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;

namespace SpringCat.NET.Network.TCP
{
	class AsyncResultSend : AsyncResult
	{
		private Link link_;

		public AsyncResultSend(Socket handle, Link link)
			: base(handle)
		{
			link_ = link;
		}

		public override void Process(uint numberOfBytesTransferred)
		{
			link_.OnSendCompleted(numberOfBytesTransferred);
		}
	}
}
