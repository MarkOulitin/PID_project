using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Concurrent;
using Opc.UaFx;
using Opc.UaFx.Client;
namespace ConsoleApp2
{
    class SamplePool
    {
        private static SamplePool _instance = null;
        public static SamplePool instance 
        {
            get
            {
                return _instance;
            }
        }

        private Dictionary<OpcNodeId, ConcurrentDictionary<DateTime, Double>> _samples;
        private SamplePool(List<OpcNodeId> plcs)
        {
            this._samples = new Dictionary<OpcNodeId, ConcurrentDictionary<DateTime, Double>>();
            foreach (OpcNodeId plc in plcs)
            {
                this._samples.Add(plc, new ConcurrentDictionary<DateTime, Double>());
            }
        }
        public static SamplePool Init(List<OpcNodeId> plcs)
        {
            _instance = new SamplePool(plcs);
            return _instance;
        }
        public void Add(OpcNodeId sensor_id, DateTime time, Double signal)
        {
            this._samples[sensor_id].GetOrAdd(time, signal);
        }

        public (List<DateTime>, List<Double>) getSamples(OpcNodeId plc)
        {
            List<DateTime> timestamps = new List<DateTime>();
            List<Double> signals = new List<Double>();
            IEnumerator<KeyValuePair<DateTime, Double>> samples_enumerator = this._samples[plc].GetEnumerator();
            while (samples_enumerator.MoveNext())
            {
                timestamps.Add(samples_enumerator.Current.Key);
                signals.Add(samples_enumerator.Current.Value);
            }
            return (timestamps, signals);
        }
    }
}
