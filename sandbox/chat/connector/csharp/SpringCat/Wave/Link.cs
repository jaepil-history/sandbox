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

			uint size = (uint)msg.Size() + sizeof(uint)*4 + sizeof(sbyte)*2;
            sbyte protocolver = 0x02;
            sbyte flag = 0;
            UInt32 crc = 0;
            binaryWriter.Write(protocolver);
            binaryWriter.Write(flag);
            binaryWriter.Write(crc);
			binaryWriter.Write(msg.RuntimeTypeInfo().Id);
            binaryWriter.Write(size);
            binaryWriter.Write(crc);

			if (!msg.Serialize(stream))
			{
				return false;
			}

			return link_.Send(stream.ToArray());
		}
        public byte[] GetSendData(IObjectBase msg)
        {
            MemoryStream stream = new MemoryStream();

            BinaryWriter binaryWriter = new BinaryWriter(stream);

            uint size = (uint)msg.Size() + sizeof(uint) * 4 + sizeof(sbyte) * 2;
            sbyte protocolver = 0x02;
            sbyte flag = 0;
            UInt32 crc = 0;
            binaryWriter.Write(protocolver);
            binaryWriter.Write(flag);
            binaryWriter.Write(crc);
            binaryWriter.Write(msg.RuntimeTypeInfo().Id);
            binaryWriter.Write(size);
            binaryWriter.Write(crc);

            if (!msg.Serialize(stream))
            {
                return null;
            }

            return stream.ToArray();
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
