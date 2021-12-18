using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CsvHelper;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Net.Http;
using System.Threading;
using Opc.UaFx;
using Opc.UaFx.Client;

namespace ConsoleApp2
{
    class PIDTask : IDisposable
    {
        public static int MathPort = 5000;
        private Double _setPoint;
        private HttpClient _httpClient;
        private SamplePool _pool;
        private OpcNodeId _plc;
        public Double setPoint 
        {
            get
            {
                return _setPoint;
            }
        }
        private PIDTask(OpcNodeId plc, Double setPoint, HttpClient httpClient, SamplePool pool)
        {
            this._setPoint = setPoint;
            this._httpClient = httpClient;
            this._pool = pool;
            this._plc = plc;
        }

        public static PIDTask Create(OpcNodeId plc, Double setPoint, SamplePool pool)
        {
            HttpClient httpClient = new HttpClient();
            return new PIDTask(plc, setPoint, httpClient, pool);
        }

        public void Dispose()
        {
            this._httpClient.Dispose();
        }

        public async Task<(Double, Double, Double)> recommendPID()
        {
            ((Double, Double), Double) inflection_gradient = await FindInflectionGradient(_pool.getSamples(this._plc));
            return CalculatePID(inflection_gradient.Item1, inflection_gradient.Item2);
        }

        private (Double, Double, Double) CalculatePID((Double, Double) inflection, Double gradient)
        {
            // inflection: point where 2nd derivative = 0 and closest to origin
            // gradient: the gradient at the point
            // Ziegler Nicols method
            // tangent: y - y1 = m(x - x1)
            // tangent_inversed: (y - y1 + mx1)/m = x
            Func<Double, Double> tangent_inversed = output => (output - inflection.Item2 + gradient * inflection.Item1) / gradient;
            Double L = tangent_inversed(0);
            Double T = tangent_inversed(this.setPoint) - L;
            Double K_p = 1.2 * (T / L);
            Double K_i = 2 * L;
            Double K_d = 0.5 * L;
            return (K_p, K_i, K_d);
        }

        private async Task<((Double, Double), Double)> FindInflectionGradient((List<DateTime>, List<Double>) samples)
        //private static async ((Double, Double), Double) findInflectionGradient(HttpClient httpClient, Tuple<List<DateTime>, List<Double>> samples)
        {
            string data = PrepareJson(samples);
            StringContent content = new StringContent(data, Encoding.UTF8, "application/json");
            HttpResponseMessage response = await this._httpClient.PostAsync($"http://127.0.0.1:{MathPort}/", content);
            JObject response_content = JObject.Parse(await response.Content.ReadAsStringAsync());
            // TODO 
            return ((0,0), 0);
        }

        private static string PrepareJson((List<DateTime>, List<Double>) samples)
        {
            JObject data = new JObject();
            data.Add("time", new JArray(samples.Item1));
            data.Add("output", new JArray(samples.Item2));
            return data.ToString(Formatting.None);
        }

       
    }
}
