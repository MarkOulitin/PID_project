export interface QueryData {
	path: string;
	minVal: number;
	maxVal: number;
}

export interface PIDNumbers {
	pVal: number;
	iVal: number;
	dVal: number;
}

export interface SimulationData {
	minutes: number;
	seconds: number;
}

export interface NavigationProps {
	state: {
		pidBefore: { p: number; i: number; d: number };
		pidAfter: { p: number; i: number; d: number };
		setPoint: number;
		graphBefore: { x: number; y: number }[];
		graphAfter: { x: number; y: number }[];
	};
}

export interface ResponseData {
	current_d: number;
	current_i: number;
	current_p: number;
	graph_after: [number, number];
	graph_before: [number, number];
	recommended_i: number;
	recommended_p: number;
	recommended_d: number;
	set_point: number;
}