using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Net;

namespace SpringCat.NET.Wave
{
	public class Link
	{
		private Network.TCP.Link link_;

		public void SetLink(Network.TCP.Link link)
		{
			link_ = link;
			link_.Data = this;
		}

		public bool Send(IObjectBase msg)
		{
			MemoryStream stream = new MemoryStream();

			BinaryWriter binaryWriter = new BinaryWriter(stream);
			uint size = (uint)msg.Size() + sizeof(uint);
			binaryWriter.Write(size);
			binaryWriter.Write(msg.RuntimeTypeInfo().Id);

			if (!msg.Serialize(stream))
			{
				return false;
			}

			return link_.Send(stream.ToArray());
		}

		public MemoryStream LockReadStream()
		{
			return link_.LockReadStream();
		}

		public void UnlockReadStream()
		{
			link_.UnlockReadStream();
		}

		public IPEndPoint GetRemoteEndPoint()
		{
			return link_.GetRemoteEndPoint();
		}

		public virtual void Close()
		{
			link_.Close();
		}
	}
}
