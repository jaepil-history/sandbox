using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.Threading;

namespace SpringCat.NET.Network.TCP
{
	public class Connector
	{
		private IOEngine engine_ = new IOEngine();
		private bool connected_ = false;
		private AutoResetEvent connectEvent_ = new AutoResetEvent(false);

		public Connector()
		{
		}

		~Connector()
		{
			Close();
		}

		public bool Connected
		{
			get
			{
				return connected_;
			}
		}

		void ConnectTimerCallback(Object stateInfo)
		{
			Console.WriteLine("[Connector] Connection time out");
			connectEvent_.Set();
		}

		void OnConnected(IAsyncResult asyncResult)
		{			
			bool connected = true;
			
			try
			{
				((Socket)asyncResult.AsyncState).EndConnect(asyncResult);
			}
			catch (System.Exception)
			{
				connected = false;
			}

			connected_ = connected;
			connectEvent_.Set();
		}

		public bool Connect(String ipAddress, int port, int timeout)
		{
			Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

			connectEvent_.Reset();
			Timer connectTimer = new Timer(new TimerCallback(ConnectTimerCallback), null, timeout, Timeout.Infinite);
			using (connectTimer)
			{
				try
				{
					socket.BeginConnect(ipAddress, port, new AsyncCallback(OnConnected), socket);
				}
				catch (System.Exception ex)
				{
					Console.WriteLine(ex.ToString());
					return false;
				}

				connectEvent_.WaitOne();
			}

			if (!connected_)
			{
				return false;
			}

			Logging.Log.Info("[Connector.Connect] connected to {0}:{1}", ipAddress, port);
			if (!engine_.PostStatus(0, new AsyncResultConnect(socket, engine_)))
			{
				engine_.RemoveActiveLinkHandle(socket);
				Logging.Log.Error("[Connector::Connect] IOEngine.PostStatus() failed.");
				return false;
			}

			return true;
		}

		public void Close()
		{
			connected_ = false;
			engine_.Close();
		}

		public void SetHandler(IOHandler handler)
		{
			engine_.SetHandler(handler);
		}
	}
}
