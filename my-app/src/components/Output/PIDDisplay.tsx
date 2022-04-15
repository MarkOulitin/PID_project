import React from "react";
import { PIDDisplayProps } from "./Output.types";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";

export const PIDDisplay: React.FC<PIDDisplayProps> = ({ pVal, iVal, dVal }) => {
	return (
		<Box
			component="form"
			sx={{
				"& > :not(style)": { m: 1, width: "35ch" },
			}}
			noValidate
			autoComplete="off"
		>
			<TextField label={"P Value"} variant="filled" value={pVal} disabled />
			<TextField label={"D Value"} variant="filled" value={iVal} disabled />
			<TextField label={"I Value"} variant="filled" value={dVal} disabled />
		</Box>
	);
};
