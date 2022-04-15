export interface DataElement {
	pathName: string;
	minScale: number;
	maxScale: number;
}
const First: DataElement = {
	pathName: "Value Path",
	minScale: 0,
	maxScale: 100,
};
const Second: DataElement = {
	pathName: "Set Point Path",
	minScale: 0,
	maxScale: 100,
};
const Third: DataElement = {
	pathName: "PID Path",
	minScale: 0,
	maxScale: 100,
};
const Forth: DataElement = {
	pathName: "PID Value Path",
	minScale: 0,
	maxScale: 100,
};
export const DataArray: DataElement[] = [First, Second, Third, Forth];

export const inputHolder = "Example PLC_L2_45_P5.L2_45_P5.410551@short";

export const pidMockBefore = {
	pVal: 5,
	iVal: 5,
	dVal: 5,
};
export const pidMockAfter = {
	pVal: 6,
	iVal: 6,
	dVal: 6,
};

export const options = {
	responsive: true,
	plugins: {
		legend: {
			position: "top" as const,
		},
		title: {
			display: true,
			text: "Chart.js Line Chart",
		},
	},
};

export const createPoints1 = () => {
	const tempArray = Array.from(Array(50).keys());
	return tempArray.map((value) => {
		return { x: value, y: value };
	});
};
export const createPoints2 = () => {
	const tempArray = Array.from(Array(50).keys());
	return tempArray.map((value) => {
		return { x: value, y: 40 };
	});
};
export const createPoints3 = () => {
	const tempArray = Array.from(Array(15).keys());
	return tempArray.map((value) => {
		return { x: value, y: value * value };
	});
};

const labels = Array.from(Array(60).keys())
	.filter((value) => value % 5 === 0)
	.map((value) => `${value}`);

export const data = {
	labels,
	datasets: [
		{
			label: "Simulation Data",
			data: createPoints1(),
			borderColor: "rgb(255, 99, 132)",
			backgroundColor: "rgba(255, 99, 132, 0.5)",
		},
		{
			label: "Set Point",
			data: createPoints2(),
			borderColor: "rgb(53, 162, 235)",
			backgroundColor: "rgba(53, 162, 235, 0.5)",
		},
	],
};
export const data2 = {
	labels,
	datasets: [
		{
			label: "Simulation Data",
			data: createPoints3(),
			borderColor: "rgb(255, 99, 132)",
			backgroundColor: "rgba(255, 99, 132, 0.5)",
		},
		{
			label: "Set Point",
			data: createPoints2(),
			borderColor: "rgb(53, 162, 235)",
			backgroundColor: "rgba(53, 162, 235, 0.5)",
		},
	],
};

// export const data2 = {
//   labels,
//   datasets: [
//     {
//       label: "Simulation Data",
//       data: createPoints1(),
//       borderColor: "rgb(255, 99, 132)",
//       backgroundColor: "rgba(255, 99, 132, 0.5)",
//     },
//     {
//       label: "Set Point",
//       data: createPoints2(),
//       borderColor: "rgb(53, 162, 235)",
//       backgroundColor: "rgba(53, 162, 235, 0.5)",
//     },
//   ],
// };

// data: {
// 		pidBefore: { p: 0, i: 0, d: 0 },
// 		pidAfter: { p: 0, i: 0, d: 0 },
// 		setPoint: 0,
// 		graphBefore: [],
// 		graphAfter: [],
// 	},
