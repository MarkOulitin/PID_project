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
namespace ConsoleApp2
{
    class Program
    {
        static void Main(string[] args)
        {
            Double set_point = 46;
            Console.WriteLine("Started...");
            HttpClient httpClient = createClient();
            using (var opcClient = new OpcClient("opc.tcp://localhost:4840"))
            {
                Console.WriteLine("Connecting...");
                opcClient.Connect();
                Console.WriteLine("Connected!");
                OpcNodeInfo node = opcClient.BrowseNode(OpcObjectTypes.ObjectsFolder);
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
                Tuple<List<DateTime>, List<Double>> samples = sample(5, sensor, opcClient);
                ((Double, Double), Double) inflection_gradient = findInflectionGradient(httpClient, samples);
                (Double, Double, Double) pid = recommendPID(set_point, inflection_gradient.Item1, inflection_gradient.Item2);
            }
            httpClient.Dispose();
        }

        private static (Double, Double, Double) recommendPID(Double set_point, (Double, Double) inflection, Double gradient)
        {
            // inflection: point where 2nd derivative = 0 and closest to origin
            // gradient: the gradient at the point
            // Ziegler Nicols method
            // tangent: y - y1 = m(x - x1)
            // tangent_inversed: (y - y1 + mx1)/m = x
            Func<Double, Double> tangent_inversed = output => (output - inflection.Item2 + gradient * inflection.Item1) / gradient;
            Double L = tangent_inversed(0);
            Double T = tangent_inversed(set_point) - L;
            Double K_p = 1.2 * (T/L);
            Double K_i = 2 * L;
            Double K_d = 0.5 * L;
            return (K_p, K_i, K_d);
        }

        private static async ((Double, Double), Double) findInflectionGradient(HttpClient httpClient, Tuple<List<DateTime>, List<Double>> samples)
        {
            string data = prepareJson(samples);
            StringContent content = new StringContent(data, Encoding.UTF8, "application/json");
            HttpResponseMessage response = await httpClient.PostAsync("http://127.0.0.1:5000/", content);
            JObject response_content = JObject.Parse(await response.Content.ReadAsStringAsync());
            return ((1, 1), 1);
        }

        private static HttpClient createClient()
        {
            return new HttpClient();
        }

        private static string prepareJson(Tuple<List<DateTime>, List<Double>> samples)
        {
            JObject data = new JObject();
            data.Add("time", new JArray(samples.Item1));
            data.Add("output", new JArray(samples.Item2));
            return data.ToString(Formatting.None);
        }

        private static Tuple<List<DateTime>, List<Double>> sample(int n, OpcNodeInfo sensor, OpcClient client)
        {
            Tuple<List<DateTime>, List<Double>> samples = Tuple.Create(new List<DateTime>(), new List<Double>());
            for (int i = 0; i < n; i++)
            {
                Tuple<DateTime, Double> data_point = (poll(client, sensor));
                samples.Item1.Add(data_point.Item1);
                samples.Item2.Add(data_point.Item2);
                Thread.Sleep(100);
            }
            return samples;
        }
        private static Tuple<DateTime, Double> poll(OpcClient client, OpcNodeInfo sensor)
        {
            DateTime request_time = DateTime.Now;
            OpcValue data = client.ReadNode(sensor.NodeId);

            return Tuple.Create(
                data.ServerTimestamp != null ? (DateTime)data.ServerTimestamp : 
                data.SourceTimestamp != null ? (DateTime)data.SourceTimestamp : request_time,
                (Double)data.Value);
        }
    }
}
