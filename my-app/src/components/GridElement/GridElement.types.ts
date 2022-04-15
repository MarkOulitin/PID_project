export interface GridElementProps {
  data: {
    pathName: string;
    minScale: number;
    maxScale: number;
    changeQueryData: (path: string, row: number, index: number) => void;
    row: number;
  };
}
