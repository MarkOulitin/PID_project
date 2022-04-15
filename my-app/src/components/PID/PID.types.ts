export interface PID {
	data: {
		pVal: number;
		iVal: number;
		dVal: number;
		changePID: (value: number, index: number) => void;
	};
}
