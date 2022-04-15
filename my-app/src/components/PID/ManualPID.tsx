import React from "react";
import { PID } from "./PID.types";
import { RowContainer, GridContainer } from "./PID.styled";
import { H2 } from "../Utils/utils.styled";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";

export const ManualPID: React.FC<PID> = ({
	data: { pVal, iVal, dVal, changePID },
}) => {
	const updatePIDValues = (e: any, index: number) => {
		changePID(e.target.value, index);
	};
	return (
		<GridContainer>
			<RowContainer>
				<H2>PID Entry</H2>
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
					label={"P"}
					value={`${pVal}`}
					onChange={(e) => updatePIDValues(e, 1)}
				/>
				<TextField
					label={"I"}
					value={`${iVal}`}
					onChange={(e) => updatePIDValues(e, 2)}
				/>

				<TextField
					label={"D"}
					value={`${dVal}`}
					onChange={(e) => updatePIDValues(e, 3)}
				/>
			</Box>
		</GridContainer>
	);
};
