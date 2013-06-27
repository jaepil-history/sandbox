using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace SpringCat.NET.Wave
{
	public interface IObjectBase
	{
		TypeInfo RuntimeTypeInfo();

		IObjectBase NewInstance();
		IObjectBase Clone();

		void Clear();

		bool Initialized();
		int Size();

		void CopyFrom(IObjectBase from);
		void MergeFrom(IObjectBase from);

		bool Serialize(Stream stream);
		bool Deserialize(Stream stream);
	}
}
