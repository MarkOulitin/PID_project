using System;
using System.Net.Sockets;
using Opc.UaFx;
using Opc.UaFx.Client;
using System.Collections.Generic;
namespace ConsoleApp2
{
    class Program
    {
        

        static void Main(string[] args)
        {
            Console.WriteLine("Started...");
            using (var client = new OpcClient("opc.tcp://localhost:4840"))
            {
                Console.WriteLine("Connecting...");
                client.Connect();
                Console.WriteLine("Connected!");
                OpcNodeInfo node = client.BrowseNode(OpcObjectTypes.ObjectsFolder);
                // PLC_L1_43_P19.L1_43_P19.425026@short
                List<OpcNodeInfo> plcs = new List<OpcNodeInfo>();
                bool flag = false;
                foreach (OpcNodeInfo childNode in node.Children())
                {
                    if (!flag)
                    {
                        flag = true;
                        continue;
                    }
                    foreach (OpcNodeInfo sensor in childNode.Children())
                    {
                        OpcValue data = client.ReadNode(sensor.NodeId);
                        Console.WriteLine("Name: {0} ID: {1} Value: {2} DataType: {3}",
                            sensor.Name, 
                            sensor.NodeId, 
                            data,
                            data.DataType);
                    }
                    //if (childNode.Name.ToString().StartsWith("PLC"))
                    //{
                    //    plcs.Add(childNode);
                    //}
                }


                //Browse(node);
                //var some = client.BrowseNodes();
                //var e = some.GetEnumerator();
                //Console.WriteLine(e.Current);
                //Console.WriteLine("--------------------------");
                //e.MoveNext();
                //Console.WriteLine(e.Current);
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
