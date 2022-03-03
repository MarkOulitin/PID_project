using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
namespace ConsoleApp2
{
    public class PythonServer
    {
        private HttpClient _httpClient;
        private int _port;

        public PythonServer(int port, HttpClient httpClient)
        {
            this._httpClient = httpClient;
            this._port = port;
        }

        public async Task<((Double, Double), Double)> FindInflectionGradient((List<DateTime>, List<Double>) samples)
        //private static async ((Double, Double), Double) findInflectionGradient(HttpClient httpClient, Tuple<List<DateTime>, List<Double>> samples)
        {
            string data = PrepareJson(samples);
            StringContent content = new StringContent(data, Encoding.UTF8, "application/json");
            HttpResponseMessage response = await this._httpClient.PostAsync($"http://127.0.0.1:{_port}/", content);
            JObject response_content = JObject.Parse(await response.Content.ReadAsStringAsync());
            // TODO 
            return ((0, 0), 0);
        }

        private static string PrepareJson((List<DateTime>, List<Double>) samples)
        {
            JObject data = new JObject();
            data.Add("time", new JArray(samples.Item1));
            data.Add("output", new JArray(samples.Item2));
            return data.ToString(Formatting.None);
        }

        internal void Dispose()
        {
            this._httpClient.Dispose();
        }
    }
}
