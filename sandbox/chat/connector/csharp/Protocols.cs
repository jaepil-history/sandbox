using System;

using JsonFx.Json;

namespace connector.Protocols
{
	public class Document<T>
	{
		public static T FromJson(string json)
		{
			var reader = new JsonReader();
			return reader.Read<T>(json);
		}
		//              public static T CreateFromJson(string json)
		//              {
		//                      return JsonMapper.ToObject<T>(json);
		//              }

		public virtual string ToJson()
		{
			var writer = new JsonWriter();
			return writer.Write(this);
		}

		public virtual byte[] ToJsonBytes()
		{
			return System.Text.Encoding.Default.GetBytes(ToJson());
		}
	}

	public class Command : Document<Command>
	{
		public string cmd;
		public string user_uid;
		public object payload;

		public override string ToJson()
		{
			var writer = new JsonWriter();
			return (writer.Write(this) + "\r\n\r\n");
		}
	}

	public class User_LoginReq : Document<User_LoginReq>
	{
		public string user_uid;
		public string user_name;
	}

	public class User_LoginAns : Document<User_LoginAns>
	{
		public User_LoginReq request;
		public Int32 error_code;
		public string error_message;
	}

	public class Message_SendReq : Document<Message_SendReq>
	{
		public string sender_uid;
		public string target_uid;
		public bool is_group;
		public string message;
	}

	public class Message_SendAns : Document<Message_SendAns>
	{
		public Message_SendReq request;
		public Int32 error_code;
		public string error_message;
	}

	public class Message_NewNoti : Document<Message_NewNoti>
	{
		public string sender_uid;
		public string message;
	}
}
