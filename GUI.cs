using Opc.UaFx;
using Opc.UaFx.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp2
{
    class GUI
    {
        private static int QUIT = -1;

        public static async void cliAsync(List<OpcNodeId> plc_ids, List<OpcNodeInfo> plcs, OpcClient client,SamplePool pool, PythonServer server)
        {
            int chosenIndex = 0;
            while (chosenIndex != -1)
            {
                chosenIndex = InputLoop(plc_ids);
                if (chosenIndex == -1)
                {
                    break;
                }
                double setPoint = promtSetpointLoop();
                OpcNodeId chosenNode = plc_ids[chosenIndex];
                PIDTask task = PIDTask.Create(chosenNode, setPoint, pool, server);
                (double, double, double) recommendation = await task.recommendPID(); //TODO should await?
                                                                                     // (double, double, double) recommendation = (1.1, 1.2, 1.3);
                PrintRecommendation(recommendation);
                Console.WriteLine("Press any key to continue.");
                Console.ReadKey();
                Console.WriteLine();
            }
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

    }
}
