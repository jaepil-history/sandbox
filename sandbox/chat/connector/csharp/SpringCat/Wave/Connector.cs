using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Threading;
using System.IO;

namespace SpringCat.NET.Wave
{
	public class Connector<LinkImplT> : Network.TCP.IOHandler
		where LinkImplT : Link, new()
	{
		private Network.TCP.Connector connector_ = new Network.TCP.Connector();
		private PacketHandler<LinkImplT> packetHandler_ = new PacketHandler<LinkImplT>();

		private AutoResetEvent connectionEvent_ = new AutoResetEvent(false);
		private Link link_;

		private const int RECV_PENDING_COUNT = 1;
		private const int RECV_BUFFER_SIZE = 1024 * 2;

		public Connector()
		{
			connector_.SetHandler(this);
		}

		public bool Connect(String ipAddress, int port, int timeout)
		{
			try
			{
				if (!connector_.Connect(ipAddress, port, timeout))
				{
					throw new System.Exception();
				}

				if (!connectionEvent_.WaitOne(timeout))
				{
					throw new System.Exception();
				}
			}
			catch (System.Exception)
			{
				Close();
				return false;
			}

			return true;
		}

		~Connector()
		{
			Close();
		}

		public bool Connected
		{
			get
			{
				return connector_.Connected;
			}
		}

		public void Close()
		{
			connector_.Close();
		}

		public Link Link
		{
			get
			{
				return link_;
			}
		}

		public bool AddDispatcher(uint key, DispatchFunction<LinkImplT> func)
		{
			return packetHandler_.AddDispatcher(key, func);
		}

		internal override void OnOpened(Network.TCP.Link link)
		{
			// Call recv function to request asynchronous data receive.
			for (uint i = 0; i < RECV_PENDING_COUNT; ++i)
			{
				link.Recv(RECV_BUFFER_SIZE);
			}

			link_ = new LinkImplT();
			link_.SetLink(link);

			connectionEvent_.Set();
		}

		internal override void OnClosed(Network.TCP.Link link)
		{
			IPEndPoint remoteEndPoint = link.GetRemoteEndPoint();
			Logging.Log.Info("[Connector] Disconnected from {0}:{1}", remoteEndPoint.Address, remoteEndPoint.Port);
			Close();
		}

		internal override void OnReceived(Network.TCP.Link link)
		{
			link.Recv(RECV_BUFFER_SIZE);

			packetHandler_.ProcessReceiveStream((LinkImplT)link.Data);
		}
	}
}
