using System;

using SpringCat.NET.Network.TCP;

using connector.Protocols;

namespace connector
{
	class ChatHandler : IOHandler
	{
		public Link active_link;

		internal override void OnOpened(Link link)
		{
			this.active_link = link;
			link.Recv(1024);
		}

		internal override void OnClosed(Link link)
		{
			this.active_link = null;
		}

		internal override void OnReceived(Link link)
		{
			var stream = link.LockReadStream();
			var buffer = new byte[stream.Length];
			stream.Read(buffer, 0, (int)stream.Length);
			Console.WriteLine(System.Text.Encoding.Default.GetString(buffer));
//			Console.Write(System.Text.Encoding.Default.GetString(stream.GetBuffer()));
//			stream.Flush();
			link.UnlockReadStream();

			link.Recv(1024);
		}
	}

	class MainClass
	{
		public static void Login(Link link, string user_uid, string user_name)
		{
			var req = new User_LoginReq();
			req.user_uid = user_uid;
			req.user_name = user_name;

			var cmd = new Command();
			cmd.cmd = "User_LoginReq";
			cmd.user_uid = user_uid;
			cmd.payload = req;

//			Console.Write(cmd.ToJson());

			link.Send(cmd.ToJsonBytes());
		}

		public static void SendMessage(Link link, string sender_uid, string target_uid, string message)
		{
			var req = new Message_SendReq();
			req.sender_uid = sender_uid;
			req.target_uid = target_uid;
			req.is_group = false;
			req.message = message;

			var cmd = new Command();
			cmd.cmd = "Message_SendReq";
			cmd.user_uid = sender_uid;
			cmd.payload = req;

//			Console.Write(cmd.ToJson());

			link.Send(cmd.ToJsonBytes());
		}

		public static void Main(string[] args)
		{
			if (args.Length != 3)
			{
				Console.WriteLine("Chat.exe [User ID] [User Name] [Target ID]");
				return;
			}

			var user_id = args[0];
			var user_name = args[1];
			var target_id = args[2];
			Console.WriteLine("{0}, {1}, {2}", user_id, user_name, target_id);

			var handler = new ChatHandler();
			var connector = new Connector();
			connector.SetHandler(handler);
			connector.Connect("chat.appengine.local.appspand.com", 20001, 1000 * 10);
			while (handler.active_link == null) {}

			Login(handler.active_link, user_id, user_name);

			Console.WriteLine("Chat client is started...");

			while (true)
			{
				Console.Write("> ");
				var line = Console.ReadLine();
				if (line.Length == 0)
				{
					continue;
				}
				if (line == "quit")
				{
					break;
				}

				SendMessage(handler.active_link, user_id, target_id, line);
			}
		}
	}
}
