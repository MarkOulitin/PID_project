import React from "react";
import {
	WidthContainer,
	GridContainerPID,
	PIDBefore,
	PIDAfter,
	GraphContainer,
	GraphsContainer,
	ColumnContainer,
} from "./Output.styled";
import { PIDDisplay } from "./PIDDisplay";
import { H1, H1Header, HeaderContainer, H2Header } from "../Utils/utils.styled";
import { Scatter } from "react-chartjs-2";
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
} from "chart.js";
import { options } from "../../MockData/Data";
import { useLocation } from "react-router-dom";

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend
);

export const Output: React.FC = () => {
	const location = useLocation();
	const { pidBefore, pidAfter, setPoint, graphBefore, graphAfter }: any =
		location.state;

	function returnData(points: any, setPoint: any) {
		const labels = Array.from(Array(60).keys())
			.filter((value) => value % 5 === 0)
			.map((value) => `${value}`);
		return {
			labels,
			datasets: [
				{
					label: "Simulation Data",
					data: points,
					borderColor: "rgb(255, 99, 132)",
					backgroundColor: "rgba(255, 99, 132, 0.5)",
				},
				{
					label: "Set Point",
					data: Array.from(Array(points.length).keys()).map((val) => {
						return { x: val, y: setPoint };
					}),
					borderColor: "rgb(53, 162, 235)",
					backgroundColor: "rgba(53, 162, 235, 0.5)",
				},
			],
		};
	}
	return (
		<WidthContainer>
			<HeaderContainer>
				<H1Header>PID Data</H1Header>
			</HeaderContainer>
			<GridContainerPID>
				<PIDBefore>
					<H1>{"Before\nCalculations"}</H1>
					<PIDDisplay {...pidBefore} />
				</PIDBefore>
				<PIDAfter>
					<H1>{"After\nCalculations"}</H1>
					<PIDDisplay {...pidAfter} />
				</PIDAfter>
			</GridContainerPID>
			<GraphsContainer>
				<ColumnContainer>
					<HeaderContainer>
						<H2Header>Old PID Data</H2Header>
					</HeaderContainer>
					<GraphContainer>
						<Scatter
							options={options}
							data={returnData(graphBefore, setPoint)}
						/>
					</GraphContainer>
				</ColumnContainer>
				<ColumnContainer>
					<HeaderContainer>
						<H2Header>New PID Data</H2Header>
					</HeaderContainer>
					<GraphContainer>
						<Scatter
							options={options}
							data={returnData(graphAfter, setPoint)}
						/>
					</GraphContainer>
				</ColumnContainer>
			</GraphsContainer>
		</WidthContainer>
	);
};
