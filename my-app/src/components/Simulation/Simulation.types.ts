export interface SimulationData {
  data: {
    minutes: number;
    seconds: number;
    changeTime: (value: number, index: number) => void;
  };
}
