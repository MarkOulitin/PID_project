import axios from "axios";
import React, { useState } from "react";
import { stringify } from "csv-stringify/sync";
import { useNavigate } from "react-router-dom";
import { DataArray } from "../../MockData/Data";
import { GridElement } from "../GridElement/GridElement";
import { PLC } from "../PLC/PLC";
import { ManualPID } from "../PID/ManualPID";
import { Simulation } from "../Simulation/Simulation";
import { Error } from "../Utils/Error";
import Loader from "../Utils/Loader";
import { H1Header, HeaderContainer } from "../Utils/utils.styled";
import {
	Button,
	GridContainer,
	WidthContainer,
	InputCSV,
	Label,
} from "./Home.styled";
import {
	PIDNumbers,
	QueryData,
	SimulationData,
	ResponseData,
} from "./Home.types";
import Send from "@mui/icons-material/Send";
import DriveFolderUploadIcon from "@mui/icons-material/DriveFolderUpload";
import Stack from "@mui/material/Stack";
import Alert from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";

export const Home: React.FC = () => {
	const statusOk = 200;
	const navigate = useNavigate();
	const [file, setFile] = useState<any>();
	const [plcPath, setPLCPath] = useState<string>("Example: XXX XXX XXX XXX");
	const [loader, setLoader] = useState<boolean>(false);
	const [errorFlag, setErrorFlag] = useState<boolean>(false);
	const [pidValues, setPidValues] = useState<PIDNumbers>({
		pVal: 0,
		iVal: 0,
		dVal: 0,
	});
	const [timeValue, setTimeValue] = useState<SimulationData>({
		minutes: 0,
		seconds: 0,
	});

	const sendQuery = () => {
		// setErrorFlag(true);
		setLoader(true);
		// setTimeout(() => {
		// 	setLoader(false);
		// 	navigate("/output", {
		// 		state: {
		// 			pidBefore: { pVal: 0, iVal: 0, dVal: 0 },
		// 			pidAfter: { pVal: 0, iVal: 0, dVal: 0 },
		// 			setPoint: 0,
		// 			graphBefore: [],
		// 			graphAfter: [],
		// 		},
		// 	});
		// }, 3000);
		console.log("log");

		// axios
		// 	.get("http://127.0.0.1:5000", {
		// 		params: {
		// 			queryData: {
		// 				valPath: "blabl",
		// 				setpointPath: "blabla",
		// 				pidPath: "bla",
		// 				pidValuePath: "blas",
		// 			},
		// 			pidValues: { ...pidValues },
		// 			timeValue: { ...timeValue },
		// 			file: file,
		// 		},
		// 	})
		// 	.then(function (response) {
		// 		if (response.status === statusOk) {
		// 			setLoader(false);
		// 			const data: ResponseData = response.data;
		// 			navigate("/output", {
		// 				state: {
		// 					pidBefore: {
		// 						pVal: data.current_p,
		// 						iVal: data.current_i,
		// 						dVal: data.current_d,
		// 					},
		// 					pidAfter: {
		// 						pVal: data.recommended_p,
		// 						iVal: data.recommended_i,
		// 						dVal: data.current_d,
		// 					},
		// 					setPoint: data.set_point,
		// 					graphBefore: data.graph_before,
		// 					graphAfter: data.graph_after,
		// 				},
		// 			});
		// 		} else {
		// 			console.log("error");
		// 		}
		// 	});
		let formData = new FormData();
		formData.append("file", file);
		formData.append("plcPath", JSON.stringify(plcPath));
		formData.append("pidValues", JSON.stringify({ ...pidValues }));
		formData.append("timeValue", JSON.stringify({ ...timeValue }));
		axios
			.post("http://127.0.0.1:5000", formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			})
			.then((response) => {
				// fnSuccess(response);
			})
			.catch((error) => {
				// fnFail(error);
			});
	};

	const changePID = (value: number, index: number) => {
		switch (index) {
			case 1:
				setPidValues({ ...pidValues, pVal: value });
				break;
			case 2:
				setPidValues({ ...pidValues, iVal: value });
				break;
			case 3:
				setPidValues({ ...pidValues, dVal: value });
				break;
		}
	};
	const changeTime = (value: number, index: number) => {
		switch (index) {
			case 1:
				setTimeValue({ ...timeValue, minutes: value });
				break;
			case 2:
				setTimeValue({ ...timeValue, seconds: value });
				break;
		}
	};
	const errorToggle = () => setErrorFlag(false);
	const onChange = (e: any) => {
		if (e !== undefined) {
			console.log("event", e);

			setFile(e?.target?.files[0]);
		}
	};

	return (
		<WidthContainer>
			{loader && <Loader />}
			{errorFlag && (
				<Error data={{ error: "Error", errorToggle: errorToggle }} />
			)}
			<HeaderContainer>
				<H1Header>OPC Query</H1Header>
			</HeaderContainer>
			<PLC
				data={{
					plcPath: plcPath,
					changePLC: setPLCPath,
				}}
			/>
			<ManualPID
				data={{
					pVal: pidValues.pVal,
					iVal: pidValues.iVal,
					dVal: pidValues.dVal,
					changePID: changePID,
				}}
			/>
			<Simulation
				data={{
					minutes: timeValue.minutes,
					seconds: timeValue.seconds,
					changeTime: changeTime,
				}}
			/>
			<Stack
				width="1200px"
				direction="column"
				justifyContent="center"
				alignItems="center"
			>
				<Stack width="80%" marginTop={"20px"}>
					<Alert severity="info">
						<AlertTitle>Info</AlertTitle>
						<strong>Fill the provided fields and upload a CSV file</strong>
					</Alert>
				</Stack>
				<Stack
					direction="row"
					justifyContent="center"
					alignItems="center"
					spacing={4}
				>
					<Button
						variant="contained"
						size="large"
						endIcon={<Send />}
						onClick={sendQuery}
						disabled={file === undefined}
					>
						Send Query
					</Button>
					<Stack direction="row" justifyContent="center" alignItems="center">
						<Label>
							<InputCSV
								type={"file"}
								id={"csvFileInput"}
								accept={".csv"}
								onChange={onChange}
							/>
							<DriveFolderUploadIcon />
							{" Upload File"}
						</Label>
					</Stack>
				</Stack>
			</Stack>
		</WidthContainer>
	);
};
