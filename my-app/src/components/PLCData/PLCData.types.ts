export interface PLCProps {
	data: {
		plcTitle: string;
		plcPath: string | undefined;
		changePLC: (value: string) => void;
	};
}
