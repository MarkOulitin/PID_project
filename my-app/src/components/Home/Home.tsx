import axios from "axios";
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { formRules } from "../../MockData/Data";
import { GridElement } from "../GridElement/GridElement";
import { PLCData } from "../PLCData/PLCData";
import { ManualPID } from "../PID/ManualPID";
import { Simulation } from "../Simulation/Simulation";
import { Error } from "../Utils/Error";
import Loader from "../Utils/Loader";
import { H1Header, HeaderContainer } from "../Utils/utils.styled";
import { Button, WidthContainer, InputCSV, Label, Span } from "./Home.styled";
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
import * as Yup from "yup";

export const validationSchema = Yup.object({
	plcPath: Yup.string().required(),
	plcSetPoint: Yup.string()
		.matches(/[+-]?\d*(\.\d+)?/, "Must be only digits")
		.optional(),
	pVal: Yup.string()
		.required()
		.matches(/[+-]?\d*(\.\d+)?/, "Must be only digits"),
	iVal: Yup.string()
		.required()
		.matches(/[+-]?\d*(\.\d+)?/, "Must be only digits"),
	dVal: Yup.string()
		.required()
		.matches(/[+-]?\d*(\.\d+)?/, "Must be only digits"),
	minutes: Yup.string()
		.required()
		.matches(/60|^[1-5]?[0-9]$/, "Must be only digits"),
	seconds: Yup.string()
		.required()
		.matches(/60|^[1-5]?[0-9]$/, "Must be only digits"),
});

export const Home: React.FC = () => {
	const statusOk = 200;
	const statusError = 500;
	const navigate = useNavigate();
	const [file, setFile] = useState<any>();
	const [plcPath, setPLCPath] = useState<string>();
	const [buttonToggle, setButtonToggle] = useState<boolean>(false);
	const [plcSetPoint, setPlcSetPoint] = useState<string>();
	const [loader, setLoader] = useState<boolean>(false);
	const [errorFlag, setErrorFlag] = useState<boolean>(false);
	const [pidValues, setPidValues] = useState<PIDNumbers>({
		pVal: "",
		iVal: "",
		dVal: "",
	});
	const [timeValue, setTimeValue] = useState<SimulationData>({
		minutes: "",
		seconds: "",
	});

	useEffect(() => {
		const validation = validationSchema.isValidSync(
			{
				plcPath: plcPath,
				plcSetPoint: plcSetPoint,
				pVal: pidValues.pVal,
				iVal: pidValues.iVal,
				dVal: pidValues.dVal,
				minutes: timeValue.minutes,
				seconds: timeValue.seconds,
			},
			{ strict: true }
		);
		setButtonToggle(validation && file !== undefined);
	}, [file, plcPath, plcSetPoint, pidValues, timeValue]);

	const test = () => {
		setTimeout(() => {
			setLoader(false);
			navigate("/output", {
				state: {
					pidBefore: { pVal: 0, iVal: 0, dVal: 0 },
					pidAfter: { pVal: 0, iVal: 0, dVal: 0 },
					setPoint: 0,
					graphBefore: [],
					graphAfter: [],
				},
			});
		}, 3000);
		// setLoader(false);
		// setErrorFlag(true);
	};
	const sendQuery = () => {
		setLoader(true);
		let formData = new FormData();
		formData.append("file", file);
		formData.append("plcPath", JSON.stringify(plcPath));
		formData.append("pidValues", JSON.stringify({ ...pidValues }));
		formData.append("timeValue", JSON.stringify({ ...timeValue }));
		formData.append("setPoint", JSON.stringify({ plcSetPoint }));
		axios
			.post("http://127.0.0.1:5000", formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			})
			.then((response) => {
				// fnSuccess(response);
				console.log("response", response);
			})
			.catch((error) => {
				console.log("error", error);
			});
	};

	const changePID = (value: string, index: number) => {
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
	const changeTime = (value: string, index: number) => {
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
		setFile(e?.target?.files[0]);
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
			<PLCData
				data={{
					plcTitle: "PLC Path",
					plcPath: plcPath,
					changePLC: setPLCPath,
				}}
			/>
			<PLCData
				data={{
					plcTitle: "PLC Set Point (Optional)",
					plcPath: plcSetPoint,
					changePLC: setPlcSetPoint,
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
						<Span>{formRules}</Span>
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
						disabled={!buttonToggle}
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
