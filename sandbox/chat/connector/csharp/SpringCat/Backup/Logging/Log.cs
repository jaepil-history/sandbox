using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SpringCat.NET.Logging
{
	public class Log
	{
		public static void Debug(String message, params Object[] args)
		{
			//Console.Write("[Debug]");
			//Console.WriteLine(message, args);
		}

		public static void Error(String message, params Object[] args)
		{
			Console.Write("[Error]");
			Console.WriteLine(message, args);
		}

		public static void Info(String message, params Object[] args)
		{
			Console.WriteLine(message, args);
		}
	}
}
