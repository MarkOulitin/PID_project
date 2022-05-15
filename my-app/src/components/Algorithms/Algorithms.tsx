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
	const [checked, setChecked] = React.useState(
		new Array(names.length).fill(false)
	);

	React.useEffect(() => {
		const copyChecked = [...checked];
		copyChecked[0] = true;
		setChecked(copyChecked);
	}, []);

	const handleChange = (
		e: React.ChangeEvent<HTMLInputElement>,
		index: number
	) => {
		const copyChecked = Array(names.length).fill(false);
		copyChecked[index] = e.target.checked;
		if (copyChecked.every((value) => !value)) {
			algorithmIndex(0);
			copyChecked[0] = true;
		} else {
			algorithmIndex(index);
		}
		setChecked(copyChecked);
	};

	return (
		<Container>
			<Box sx={{ display: "flex", flexDirection: "row", ml: 3 }}>
				{names.map((name: string, index: number) => {
					return (
						<FormControlLabel
							label={name}
							control={
								<Checkbox
									checked={checked[index]}
									onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
										handleChange(e, index)
									}
								/>
							}
						/>
					);
				})}
			</Box>
		</Container>
	);
};
