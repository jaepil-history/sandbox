using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace SpringCat.NET.Network.TCP
{
	using ActiveLinkListT = List<Link>;

	public class Acceptor
	{
		private List<AcceptorTask> acceptorTasks_ = new List<AcceptorTask>();
		private IOEngine engine_ = new IOEngine();

		public Acceptor()
		{
		}

		~Acceptor()
		{
			Console.WriteLine("Acceptor.~Acceptor()");
			ClearBindings();
		}

		public bool Start()
		{
			if (!Stop())
			{
				return false;
			}

			bool result = true;

			lock (this)
			{
				foreach (AcceptorTask acceptorTask in acceptorTasks_)
				{
					if (!acceptorTask.Start())
					{
						result = false;
					}
				}
			}

			return result;
		}

		public bool Stop()
		{
			lock (this)
			{
				foreach (AcceptorTask acceptorTask in acceptorTasks_)
				{
					acceptorTask.Stop();
				}
			}

			return true;
		}

		public bool AddBinding(String ipAddress, int port, bool reuse)
		{
			if (0 == ipAddress.Length)
			{
				ipAddress = Consts.anyAddress_;
			}

			lock (this)
			{
				foreach (AcceptorTask acceptorTask in acceptorTasks_)
				{
					if (acceptorTask.GetIpAddress() == ipAddress && acceptorTask.GetPort() == port)
					{
						return false;
					}
				}

				acceptorTasks_.Add(new AcceptorTask(ipAddress, port, reuse, engine_));
			}

			return true;
		}

		public bool RemoveBinding(String ipAddress, ushort port)
		{
			if (0 == ipAddress.Length)
			{
				ipAddress = Consts.anyAddress_;
			}

			lock (this)
			{
				for (int i = 0; i < acceptorTasks_.Count; ++i)
				{
					AcceptorTask acceptorTask = acceptorTasks_[i];
					if (acceptorTask.GetIpAddress() == ipAddress && acceptorTask.GetPort() == port)
					{
						acceptorTasks_.RemoveAt(i);
						return true;
					}
				}
			}

			return false;
		}

		public void ClearBindings()
		{
			lock (this)
			{
				acceptorTasks_.Clear();
			}
		}

		public void SetHandler(IOHandler handler)
		{
			engine_.SetHandler(handler);
		}
	}
}
