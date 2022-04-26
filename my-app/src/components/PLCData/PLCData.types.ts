export interface PLCProps {
	data: {
		plcTitle: string;
		plcPath: string;
		changePLC: (value: string) => void;
	};
}
