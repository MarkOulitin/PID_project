﻿using System;
using System.Net.Sockets;
using Opc.UaFx;
using Opc.UaFx.Client;
using System.Collections.Generic;
using System.Timers;
using System.Threading;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text;
//using System.Text.Json;
// https://www.newtonsoft.com/json/help/html/T_Newtonsoft_Json_Linq_JValue.htm
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Collections.Specialized;
using McMaster.Extensions.CommandLineUtils;
namespace ConsoleApp2
{
    class Program
    {
        public static readonly string opc_url = "opc.tcp://localhost:4840";
        public static string opc_ip = "localhost";
        public static string opc_port = "4840";
        public static string MathAPI_port = "localhost";
        public static string System_port = "localhost";
        private static SamplePool _pool = null;
        public static SamplePool pool
        {
            get
            {
                return _pool;
            }
        }
        static void Main(string[] args)
        {
            readConfig();
            setupMathAPI();
            using (var client = new OpcClient(opc_url))
            {
                Console.WriteLine("Connecting...");
                client.Connect();
                Console.WriteLine("Connected!");
                List<OpcNodeInfo> plcs = discoverPLCS(client);
                List<OpcNodeId> plc_ids = new List<OpcNodeId>();
                plcs.ForEach(plc => plc_ids.Add(plc.NodeId));
                _pool = SamplePool.Init(plc_ids);
                Sampler sampler = Sampler.Create(opc_url, plcs[0], pool);
                cli(plc_ids);
            }
        }

        private static void readConfig()
        {

        }

        private static void setupMathAPI()
        {

        }

        private static int cli(List<OpcNodeId> plc_ids)
        {
            //var app = new CommandLineApplication();

            //app.HelpOption();
            //var subject = app.Option("-s|--subject <SUBJECT>", "The subject", CommandOptionType.SingleValue);
            ////subject.De = "world";

            //app.OnExecute(() =>
            //{
            //    Console.WriteLine($"Hello {subject.Value()}!");
            //    return 0;
            //});




            //return app.Execute();
            return 0;
        }

        private static List<OpcNodeInfo> discoverPLCS(OpcClient client)
        {
            OpcNodeInfo node = client.BrowseNode(OpcObjectTypes.ObjectsFolder);
            // PLC_L1_43_P19.L1_43_P19.425026@short
            List<OpcNodeInfo> plcs = new List<OpcNodeInfo>();
            IEnumerator<OpcNodeInfo> plc_enumerator = node.Children().GetEnumerator();
            plc_enumerator.MoveNext(); // Now point on first child
            plc_enumerator.MoveNext();
            OpcNodeInfo plc = plc_enumerator.Current;
            Console.WriteLine("Name: {0} ID: {1}",
                plc.Name,
                plc.NodeId);
            IEnumerator<OpcNodeInfo> sensors_enumerator = plc.Children().GetEnumerator();
            sensors_enumerator.MoveNext();
            OpcNodeInfo sensor = sensors_enumerator.Current;
            List<OpcNodeInfo> output = new List<OpcNodeInfo>();
            output.Add(sensor);
            return output;
        }

    }
}
