export interface SimulationData {
  data: {
    minutes: string;
    seconds: string;
    changeTime: (value: string, index: number) => void;
  };
}
