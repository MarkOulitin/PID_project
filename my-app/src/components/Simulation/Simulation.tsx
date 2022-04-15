import React from "react";
import { SimulationData } from "./Simulation.types";
import { GridContainer, RowContainer } from "../PID/PID.styled";
import { H2 } from "../Utils/utils.styled";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";

export const Simulation: React.FC<SimulationData> = ({
	data: { minutes, seconds, changeTime },
}) => {
	const updateTime = (e: any, index: number) => {
		changeTime(e.target.value, index);
	};
	return (
		<GridContainer>
			<RowContainer>
				<H2>Simulation Data</H2>
			</RowContainer>
			<Box
				border={"1px solid black"}
				component="form"
				sx={{
					"& > :not(style)": { m: 3, width: "35ch" },
				}}
				noValidate
				autoComplete="off"
			>
				<TextField
					label={"Minutes"}
					onChange={(e) => updateTime(e, 1)}
					value={minutes}
				/>
				<TextField
					label={"Seconds"}
					value={seconds}
					onChange={(e) => updateTime(e, 2)}
				/>
			</Box>
		</GridContainer>
	);
};
