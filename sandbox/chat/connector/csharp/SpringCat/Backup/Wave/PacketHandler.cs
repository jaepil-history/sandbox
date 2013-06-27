using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Net;

namespace SpringCat.NET.Wave
{
	public class PacketHandler<LinkImplT> where LinkImplT : Link
	{
		private Dispatcher<LinkImplT> dispatcher_ = new Dispatcher<LinkImplT>();

		public void ProcessReceiveStream(LinkImplT link)
		{
			try
			{
				MemoryStream stream = link.LockReadStream();
				for (; ; )
				{
					uint id = 0;
					byte[] messageBlockStream = null;
					long rollBackPos;
					if (!ProtocolParser.ExtractMessage(stream, out id, out messageBlockStream, out rollBackPos))
					{
						break;
					}

					if (!dispatcher_.Dispatch(id, link, new MemoryStream(messageBlockStream)))
					{
						stream.Seek(rollBackPos, SeekOrigin.Begin);
						Logging.Log.Error("[Wave.Acceptor] Unknown message id: {0:X}", id);
						throw new System.Exception();
					}
				}
			}
			catch(System.Exception)
			{
				link.Close();
			}
			finally
			{
				link.UnlockReadStream();
			}
		}

		public bool AddDispatcher(uint key, DispatchFunction<LinkImplT> func)
		{
			return dispatcher_.Add(key, func);
		}
	}
}
