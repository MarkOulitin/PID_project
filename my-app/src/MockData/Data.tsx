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

export const formRules =
	"Fill the provided fields and upload a CSV file.\nPLC Path should be informative.\nPLC Set Point is optional.\nPID Values should be valid.\nSimulation Data values should be valid.\nAlgorithm must be selected, or a default will be used.";
