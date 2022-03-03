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
        private PythonServer _mathServer;
        private SamplePool _pool;
        private OpcNodeId _plc;
        public Double setPoint 
        {
            get
            {
                return _setPoint;
            }
        }

        private PIDTask(OpcNodeId plc, Double setPoint, PythonServer mathServer, SamplePool pool)
        {
            this._setPoint = setPoint;
            this._mathServer = mathServer;
            this._pool = pool;
            this._plc = plc;
        }

        public static PIDTask Create(OpcNodeId plc, Double setPoint, SamplePool pool, PythonServer mathServer)
        {
            return new PIDTask(plc, setPoint, mathServer, pool);
        }

        public void Dispose()
        {
            this._mathServer.Dispose();
        }

        public async Task<(Double, Double, Double)> recommendPID()
        {
            ((Double, Double), Double) inflection_gradient = await _mathServer.FindInflectionGradient(_pool.getSamples(this._plc));
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
       
    }
}
