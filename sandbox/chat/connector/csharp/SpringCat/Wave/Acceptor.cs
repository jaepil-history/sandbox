using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.IO;

namespace SpringCat.NET.Wave
{
	public class Acceptor<LinkImplT> : Network.TCP.IOHandler
		where LinkImplT : Link, new()
	{
		private Network.TCP.Acceptor acceptor_ = new Network.TCP.Acceptor();
		private PacketHandler<LinkImplT> packetHandler_ = new PacketHandler<LinkImplT>();

		private const int RECV_PENDING_COUNT = 1;
		private const int RECV_BUFFER_SIZE = 1024 * 2;

		public Acceptor(int port)
		{
			acceptor_.SetHandler(this);
			acceptor_.AddBinding("", port, true);
		}

		~Acceptor()
		{
			Stop();
		}

		public bool Start()
		{
			return acceptor_.Start();
		}

		public bool Stop()
		{
			return acceptor_.Stop();
		}

		internal override void OnOpened(Network.TCP.Link link)
		{
			LinkImplT linkImpl = null;
			try
			{
				linkImpl = new LinkImplT();
			}
			catch
			{
				link.Close();
				return;
			}

			linkImpl.SetLink(link);

			IPEndPoint remoteEndPoint = link.GetRemoteEndPoint();
			if (remoteEndPoint != null)
			{
				Logging.Log.Info("[Wave.Acceptor] Link accepted: {0}:{1}", remoteEndPoint.Address.ToString(), remoteEndPoint.Port.ToString());
			}

			link.SetNoDelay(true);

			for (uint i = 0; i < RECV_PENDING_COUNT; ++i)
			{
				link.Recv(RECV_BUFFER_SIZE);
			}
		}

		internal override void OnClosed(Network.TCP.Link link)
		{
			IPEndPoint remoteEndPoint = link.GetRemoteEndPoint();
			if (remoteEndPoint != null)
			{
				Logging.Log.Info("[Wave.Acceptor] Link closed: {0}:{1}", remoteEndPoint.Address.ToString(), remoteEndPoint.Port.ToString());
			}
		}

		internal override void OnReceived(Network.TCP.Link link)
		{
			link.Recv(RECV_BUFFER_SIZE);

			packetHandler_.ProcessReceiveStream((LinkImplT)link.Data);
		}

		public bool AddDispatcher(uint key, DispatchFunction<LinkImplT> func)
		{
			return packetHandler_.AddDispatcher(key, func);
		}
	}
}