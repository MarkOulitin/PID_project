using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Timers;
using System.Threading;
using Opc.UaFx;
using Opc.UaFx.Client;
using CsvHelper;
namespace ConsoleApp2
{
    class Sampler : IDisposable
    {
        private OpcNodeInfo _sensor;
        private OpcClient _client;
        private int persist_counter = 0;
        private List<Tuple<DateTime, Double>> _samples;
        private System.Timers.Timer _timer;
        private SamplePool _pool;
        private Sampler(OpcClient client, OpcNodeInfo sensor, SamplePool pool)
        {
            this._sensor = sensor;
            this._client = client;
            this._pool = pool;
            this._samples = new List<Tuple<DateTime, double>>();
            this._timer = new System.Timers.Timer();
            this._timer.Interval = 1000;
            this._timer.Elapsed += Sample;
            this._timer.AutoReset = true;
        }

        public static Sampler Create(string url, OpcNodeInfo sensor, SamplePool pool)
        {
            OpcClient client = new OpcClient(url);
            client.Connect();
            return new Sampler(client, sensor, pool);
        }
        public void sample()
        {
            this._timer.Enabled = true;
        }
        private void Sample(Object source, ElapsedEventArgs e)
        {
            Tuple<DateTime, Double> data_point = Poll(this._client, this._sensor);
            this._pool.Add(this._sensor.NodeId, data_point.Item1, data_point.Item2);
            this._samples.Add(data_point);
            if (++this.persist_counter > 20)
            {
                persist_counter = 0;
                Save();
            }
        }

        private void Save()
        {
            //using (Stream)
            //{

            //}
        }

        public void Dispose()
        {
            this._client.Dispose();
        }

        private static Tuple<DateTime, Double> Poll(OpcClient client, OpcNodeInfo sensor)
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
