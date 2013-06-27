using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace SpringCat.NET.Wave
{
	public delegate void DispatchFunction<LinkImplT>(LinkImplT link, Stream stream);

	public class Dispatcher<LinkImplT>
	{
		private Dictionary<uint, DispatchFunction<LinkImplT>> functors_ = new Dictionary<uint, DispatchFunction<LinkImplT>>();

		public bool Add(uint id, DispatchFunction<LinkImplT> func)
		{
			if (functors_.ContainsKey(id))
			{
				Logging.Log.Error("[Dispatcher.Add] duplicated id {0}", id);
				return false;
			}

			functors_[id] = func;

			return true;
		}

		public bool Dispatch(uint id, LinkImplT link, Stream stream)
		{
			if (!functors_.ContainsKey(id))
			{
				return false;
			}

			//Logging.Log.Info("[Dispatcher.Dispatch] Dispatched message {0}.", functors_[id].Method.ToString());
			functors_[id](link, stream);
			return true;
		}
	}
}
