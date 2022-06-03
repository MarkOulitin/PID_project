import React from "react";
import { PLCProps } from "./PLCData.types";
import { GridContainer, RowContainer } from "../PID/PID.styled";
import { H2 } from "../Utils/utils.styled";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";

export const PLCData: React.FC<PLCProps> = ({
	data: { plcTitle, plcPath, changePLC },
}) => {
	return (
		<GridContainer>
			<RowContainer>
				<H2>{plcTitle}</H2>
			</RowContainer>
			<Box
				border={"1px solid black"}
				component="form"
				sx={{
					"& > :not(style)": { m: 3, width: "94%" },
				}}
				noValidate
				autoComplete="off"
			>
				<TextField
					label={plcTitle}
					value={plcPath ?? ""}
					onChange={(e) => changePLC(e.target.value)}
				/>
			</Box>
		</GridContainer>
	);
};
