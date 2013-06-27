using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SpringCat.NET.Network.TCP
{
	public abstract class IOHandler
	{
		internal abstract void OnOpened(Link link);
		internal abstract void OnClosed(Link link);
		internal abstract void OnReceived(Link link);
	}
}
