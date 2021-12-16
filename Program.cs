using System;
using System.Net.Sockets;
using Opc.UaFx;
using Opc.UaFx.Client;
namespace ConsoleApp2
{
    class Program
    {
        

        static void Main(string[] args)
        {
            using (var client = new OpcClient("opc.tcp://localhost:4840"))
            {
                client.Connect();

                var node = client.BrowseNode(OpcObjectTypes.ObjectsFolder);
                Browse(node);

                //OpcValue value = client.ReadNode("ns=2;i=2");
                //if (value.Status.IsGood)
                //{
                //    double intvalue = (double)value.Value;
                //    Console.WriteLine("value", intvalue);
                //}
                //else
                //{
                //    Console.WriteLine("bad");
                //}
            }
        }
        private static void Browse(OpcNodeInfo node, int level = 0)
        {
            Console.WriteLine("{0}{1}({2})",
                    new string('.', level * 4),
                    node.Attribute(OpcAttribute.DisplayName).Value,
                    node.NodeId);

            level++;

            foreach (var childNode in node.Children())
                Browse(childNode, level);
        }
    }
}
