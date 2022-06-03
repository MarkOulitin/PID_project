import React from "react";
import Box from "@mui/material/Box";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import { AlgorithmProps } from "./Algorithm.types";
import { Container } from "./Algorithm.styled";

export const Algorithms: React.FC<AlgorithmProps> = ({
	names,
	algorithmIndex,
}) => {
	const [checked, setChecked] = React.useState(0);

	return (
		<Container>
			<Box sx={{ display: "flex", flexDirection: "row", ml: 3 }}>
				{names &&
					names.map((name: string, index: number) => {
						return (
							<FormControlLabel
								key={name}
								label={name}
								control={
									<Checkbox
										checked={index === checked ? true : false}
										onChange={() => setChecked(index)}
									/>
								}
							/>
						);
					})}
			</Box>
		</Container>
	);
};
