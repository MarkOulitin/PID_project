using System;
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
        private static int QUIT = -1;
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
                ConnectClient(client);
                List<OpcNodeInfo> plcs = discoverPLCS(client);
                List<OpcNodeId> plc_ids = ExtractPlcIDs(plcs);
                //---------------------- Delete: -----------------------------
                //List < OpcNodeInfo > plcs= new();
                //List<OpcNodeId> plc_ids = new();
                //plc_ids.Add(new OpcNodeId(new byte[] { 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20 }));
                //--------------------- /Delete: -----------------------------
                InitPool(plc_ids);
                Sampler sampler = Sampler.Create(opc_url, plcs[0], pool);
                cliAsync(plc_ids, plcs, client);
            }
        }

        private static void InitPool(List<OpcNodeId> plc_ids)
        {
            _pool = SamplePool.Init(plc_ids);
        }

        private static List<OpcNodeId> ExtractPlcIDs(List<OpcNodeInfo> plcs)
        {
            List<OpcNodeId> plc_ids = new List<OpcNodeId>();
            plcs.ForEach(plc => plc_ids.Add(plc.NodeId));
            return plc_ids;
        }

        private static void ConnectClient(OpcClient client)
        {
            Console.WriteLine("Connecting...");
            client.Connect();
            Console.WriteLine("Connected!");
        }

        private static void readConfig()
        {

        }

        private static void setupMathAPI()
        {

        }

        private static async void cliAsync(List<OpcNodeId> plc_ids, List<OpcNodeInfo> plcs, OpcClient client)
        {
            int chosenIndex = 0;
            while(chosenIndex != -1)
            {
                chosenIndex = InputLoop(plc_ids);
                if(chosenIndex == -1)
                {
                    break;
                }
                double setPoint = promtSetpointLoop();
                OpcNodeId chosenNode = plc_ids[chosenIndex];
                PIDTask task = PIDTask.Create(chosenNode, setPoint, pool);
                (double, double, double) recommendation = await task.recommendPID(); //TODO should await?
                //(double, double, double) recommendation = (1.1, 1.2, 1.3);
                PrintRecommendation(recommendation);
                Console.WriteLine("Press any key to continue.");
                Console.ReadKey();
                Console.WriteLine();
            }


        }

        private static void PrintRecommendation((double, double, double) recommendation)
        {
            double p = recommendation.Item1;
            double i = recommendation.Item2;
            double d = recommendation.Item3;
            Console.WriteLine("Recommended P value: {0}", p);
            Console.WriteLine("Recommended I value: {0}", i);
            Console.WriteLine("Recommended D value: {0}", d);
        }

        private static double promtSetpointLoop()
        {
            bool validUserInput = false;
            double userInput = -1;
            while (validUserInput == false)
            {
                try
                {
                    userInput = PromtsetpointInput();
                }
                catch (Exception)
                {
                    Console.WriteLine("Input must be a number. Try again.");
                    continue;
                }

                if (IsValidSetpointInput(userInput))
                {
                    validUserInput = true;
                }
                else
                {
                    Console.WriteLine("Invalid input. Try again.");
                }

            }
            return userInput;
        }

        private static bool IsValidSetpointInput(double userInput)
        {
            return true; //TODO needs further validation?
        }

        private static double PromtsetpointInput()
        {
            double userInput;
            Console.WriteLine("Enter setpoint:  ");
            userInput = double.Parse(Console.ReadLine());
            return userInput;
        }

        private static int InputLoop(List<OpcNodeId> plc_ids)
        {
            int intUserInput = 0;
            bool validUserInput = false;
            while (validUserInput == false)
            {
                try
                {
                    intUserInput = PromtUserInput(plc_ids);
                }
                catch (Exception)
                {
                    Console.WriteLine("Input must be a number. Try again.");
                    continue;
                }

                if (IsValidInput(intUserInput, plc_ids.Count))
                {
                    validUserInput = true;
                }
                else
                {
                    Console.WriteLine("Chosen index out of bounds. Try again.");
                }

            }
            return intUserInput;
        }

        private static int PromtUserInput(List<OpcNodeId> plc_ids)
        {
            int idIndex = 0;
            int intUserInput;
            Console.WriteLine("Choose a controller, or type {0} to quit:", QUIT);
            plc_ids.ForEach(id => {
                Console.WriteLine("{0}. {1}", idIndex, id.ToString());
            });
            intUserInput = int.Parse(Console.ReadLine());
            return intUserInput;
        }

        private static bool IsValidInput(int intUserInput, int listLength)
        {
            return intUserInput == QUIT || (intUserInput >= 0 && intUserInput < listLength);
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
