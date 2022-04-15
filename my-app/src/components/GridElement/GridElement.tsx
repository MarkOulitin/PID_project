import { inputHolder } from "../../MockData/Data";
import {
	H1,
	Input,
	InputMinMax,
	InputPath,
	Path,
	Range,
} from "./GridElement.styled";
import { GridElementProps } from "./GridElement.types";

export const GridElement = ({ data }: GridElementProps) => {
	const changeData = (e: any, index: number) => {
		data.changeQueryData(e.target.value, data.row, index);
	};

	return (
		<>
			<Path>
				<H1>{data.pathName}</H1>
			</Path>
			<Input>
				<InputPath
					onChange={(e) => changeData(e, 1)}
					placeholder={inputHolder}
					type="text"
				/>
			</Input>
			<Range>
				<H1>Min</H1>
				<InputMinMax
					onChange={(e) => changeData(e, 2)}
					placeholder={`${data.minScale}`}
					type="number"
				/>
				<InputMinMax
					onChange={(e) => changeData(e, 3)}
					placeholder={`${data.maxScale}`}
					type="number"
				/>
				<H1>Max</H1>
			</Range>
		</>
	);
};
