using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace SpringCat.NET.Wave
{
	public static class ProtocolParser
	{
		public static bool ExtractMessage(Stream stream, out uint id, out byte[] messageBlockStream, out long rollBackPos)
		{
			id = 0;
			messageBlockStream = null;

			rollBackPos = stream.Position;

			BinaryReader reader = new BinaryReader(stream);
			try
			{
				if (stream.Length - stream.Position <= sizeof(uint))
				{
					throw new System.Exception();
				}

				uint length = reader.ReadUInt32();
				if (stream.Length - stream.Position < length)
				{
					throw new System.Exception();
				}

				id = reader.ReadUInt32();
				messageBlockStream = reader.ReadBytes((int)length - sizeof(uint));
			}
			catch (System.Exception)
			{
				stream.Seek(rollBackPos, SeekOrigin.Begin);
				byte[] remainingData = reader.ReadBytes((int)(stream.Length - rollBackPos));
				stream.Seek(0, SeekOrigin.Begin);
				BinaryWriter writer = new BinaryWriter(stream);
				writer.Write(remainingData);
				stream.Seek(0, SeekOrigin.Begin);
				stream.SetLength(remainingData.Length);
				MemoryStream memoryStream = stream as MemoryStream;
				if (memoryStream != null)
				{
					memoryStream.Capacity = remainingData.Length;
				}
				return false;
			}

			return true;
		}
	}
}
