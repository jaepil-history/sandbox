using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;

namespace SpringCat.NET.Network.TCP
{
	class AsyncResultRecv : AsyncResult
	{
		private byte[] buffer_;
		private ulong ioSeq_;
		private Link link_;

		public AsyncResultRecv(Socket handle, byte[] buffer, ulong ioSeq, Link link)
			: base(handle)
		{
				buffer_ = buffer;
				ioSeq_ = ioSeq;
				link_ = link;
		}

		public override void Process(uint numberOfBytesTransferred)
		{
			link_.OnReceiveCompleted(ioSeq_, buffer_, numberOfBytesTransferred);
		}
	}
}
