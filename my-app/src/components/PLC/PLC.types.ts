export interface PLCProps {
  data: {
    plcPath: string;
    changePLC: (value:string) => void;
  };
}
