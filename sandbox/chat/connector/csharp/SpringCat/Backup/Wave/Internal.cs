using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace SpringCat.NET.Wave
{
	public class Internal
	{
		public static bool Deserialize(BinaryReader input, out String value)
		{
			value = "";
			try
			{
				uint size = input.ReadUInt32();
				value = Encoding.UTF8.GetString(input.ReadBytes((int)size));
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out bool value)
		{
			value = false;
			try
			{
				value = input.ReadBoolean();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out Int16 value)
		{
			value = 0;
			try
			{
				value = input.ReadInt16();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out Int32 value)
		{
			value = 0;
			try
			{
				value = input.ReadInt32();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out Int64 value)
		{
			value = 0;
			try
			{
				value = input.ReadInt64();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out UInt16 value)
		{
			value = 0;
			try
			{
				value = input.ReadUInt16();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out UInt32 value)
		{
			value = 0;
			try
			{
				value = input.ReadUInt32();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out UInt64 value)
		{
			value = 0;
			try
			{
				value = input.ReadUInt64();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out float value)
		{
			value = 0.0f;
			try
			{
				value = input.ReadSingle();
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, out byte[] value)
		{
			value = new byte[0];
			try
			{
				uint size = input.ReadUInt32();
				value = input.ReadBytes((int)size);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Deserialize(BinaryReader input, IObjectBase value)
		{
			value = null;
			try
			{
				value.Deserialize(input.BaseStream);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, String value)
		{
			try
			{
				byte[] utf8_value = Encoding.UTF8.GetBytes(value);
				output.Write((uint)utf8_value.Length);
				output.Write(utf8_value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, bool value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, Int16 value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, Int32 value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, Int64 value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, UInt16 value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, UInt32 value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, UInt64 value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, float value)
		{
			try
			{
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, byte[] value)
		{
			try
			{
				output.Write((uint)value.Length);
				output.Write(value);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		public static bool Serialize(BinaryWriter output, IObjectBase value)
		{
			try
			{
				value.Serialize(output.BaseStream);
			}
			catch (System.Exception)
			{
				return false;
			}

			return true;
		}

		// Size
		public static int Size(bool value)
		{
			return sizeof(bool);
		}
		public static int Size(sbyte value)
		{
			return sizeof(sbyte);
		}
		public static int Size(short value)
		{
			return sizeof(short);
		}
		public static int Size(int value)
		{
			return sizeof(int);
		}
		public static int Size(long value)
		{
			return sizeof(long);
		}
		public static int Size(byte value)
		{
			return sizeof(byte);
		}
		public static int Size(ushort value)
		{
			return sizeof(ushort);
		}
		public static int Size(uint value)
		{
			return sizeof(uint);
		}
		public static int Size(ulong value)
		{
			return sizeof(ulong);
		}
		public static int Size(float value)
		{
			return sizeof(float);
		}
		public static int Size(double value)
		{
			return sizeof(double);
		}
		public static int Size(String value)
		{
			int size = sizeof(uint);
			size += value.Length;

			return size;
		}
		public static int Size(IObjectBase message)
		{
			return message.Size();
		}
	}
}
