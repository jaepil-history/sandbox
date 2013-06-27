using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace SpringCat.NET.Network.TCP
{
	class AcceptorTask
	{
		private IPEndPoint ipEndPoint_;
		private Socket socket_;
		private Thread thread_;
		private IOEngine engine_;

		public AcceptorTask(String ipAddress, int port, bool reuse, IOEngine engine)
		{
			ipEndPoint_ = new IPEndPoint(IPAddress.Parse(ipAddress), port);
			engine_ = engine;
		}

		~AcceptorTask()
		{
			Stop();
		}

		public String GetIpAddress()
		{
			return ipEndPoint_.Address.ToString();
		}

		public int GetPort()
		{
			return ipEndPoint_.Port;
		}

		public bool Start()
		{
			if (!Stop())
			{
				Logging.Log.Error("[AcceptorTask::Start()] Stop failed.");
				return false;
			}

			try
			{
				socket_ = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
				socket_.Bind(ipEndPoint_);
			}
			catch (System.Exception ex)
			{
				Stop();
				Logging.Log.Error("[AcceptorTask::Start()] Socket.Bind failed. {0}", ex.ToString());
				return false;
			}

			try
			{
				socket_.Listen((int)SocketOptionName.MaxConnections);
			}
			catch (System.Exception)
			{
				Stop();
				Logging.Log.Error("[AcceptorTask::Start()] Socket.Listen failed.");
				return false;
			}

			thread_ = new Thread(new ParameterizedThreadStart(DoExecute));
			thread_.Start(this);

			return true;
		}

		public bool Stop()
		{
			if (socket_ != null)
			{
				socket_.Close();
				socket_ = null;
			}

			if (thread_ != null)
			{
				thread_.Abort();
				thread_ = null;
			}

			return true;
		}

		public void Execute()
		{
			for (; ; )
			{
				Socket handle = socket_.Accept();

				engine_.AddActiveLinkHandle(handle);

				if (!engine_.PostStatus(0, new AsyncResultConnect(handle, engine_)))
				{
					engine_.RemoveActiveLinkHandle(handle);
					handle.Close();
					Logging.Log.Error("[AcceptorTask.Execute()] IOEngine.PostStatus failed");
					continue;
				}
			}
		}

		public static void DoExecute(Object context)
		{
			AcceptorTask acceptorTask = (AcceptorTask)context;
			acceptorTask.Execute();
		}
	}
}
