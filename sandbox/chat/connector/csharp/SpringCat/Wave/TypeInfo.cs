using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SpringCat.NET.Wave
{
	public class TypeInfo
	{
		private uint id_;
		private String name_;

		public TypeInfo(uint id, String name)
		{
			id_ = id;
			name_ = name;
		}

		public uint Id
		{
			get
			{
				return id_;
			}
		}

		public String Name
		{
			get
			{
				return name_;
			}
		}
	}
}
