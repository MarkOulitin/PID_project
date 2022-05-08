export interface PID {
	data: {
		pVal: string;
		iVal: string;
		dVal: string;
		changePID: (value: string, index: number) => void;
	};
}
