import axios from "axios";
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { formRules } from "../../MockData/Data";
import { PLCData } from "../PLCData/PLCData";
import { Algorithms } from "../Algorithms/Algorithms";
import { ManualPID } from "../PID/ManualPID";
import { Simulation } from "../Simulation/Simulation";
import { Error } from "../Utils/Error";
import Loader from "../Utils/Loader";
import { H1Header, HeaderContainer } from "../Utils/utils.styled";
import { Button, WidthContainer, InputFile, Label, Span } from "./Home.styled";
import { PIDNumbers, SimulationData, Response } from "./Home.types";
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
		.matches(
			/^(?!(?:^[-+]?[0.]+(?:[Ee]|$)))(?!(?:^-))(?:(?:[+-]?)(?=[0123456789.])(?:(?:(?:[0123456789]+)(?:(?:[.])(?:[0123456789]*))?|(?:(?:[.])(?:[0123456789]+))))(?:(?:[Ee])(?:(?:[+-]?)(?:[0123456789]+))|))$/,
			"Must be only digits"
		),
	iVal: Yup.string()
		.required()
		.matches(
			/^(?!(?:^[-+]?[0.]+(?:[Ee]|$)))(?!(?:^-))(?:(?:[+-]?)(?=[0123456789.])(?:(?:(?:[0123456789]+)(?:(?:[.])(?:[0123456789]*))?|(?:(?:[.])(?:[0123456789]+))))(?:(?:[Ee])(?:(?:[+-]?)(?:[0123456789]+))|))$/,
			"Must be only digits"
		),
	dVal: Yup.string()
		.required()
		.matches(
			/^(?!(?:^[-+]?[0.]+(?:[Ee]|$)))(?!(?:^-))(?:(?:[+-]?)(?=[0123456789.])(?:(?:(?:[0123456789]+)(?:(?:[.])(?:[0123456789]*))?|(?:(?:[.])(?:[0123456789]+))))(?:(?:[Ee])(?:(?:[+-]?)(?:[0123456789]+))|))$/,
			"Must be only digits"
		),
	minutes: Yup.string()
		.required()
		.matches(/60|^[1-5]?[0-9]$/, "Must be only digits"),
	seconds: Yup.string()
		.required()
		.matches(/60|^[1-5]?[0-9]$/, "Must be only digits"),
});

export const Home: React.FC = () => {
	const statusOk = 200;
	const navigate = useNavigate();
	const [algorithmNames, setAlgorithmNames] = useState<string[]>([
		"No algorithms available",
	]);
	const [file, setFile] = useState<any>();
	const [algoFile, setAlgoFile] = useState<any>();
	const [plcPath, setPLCPath] = useState<string>();
	const [buttonToggle, setButtonToggle] = useState<boolean>(false);
	const [plcSetPoint, setPlcSetPoint] = useState<string>();
	const [loader, setLoader] = useState<boolean>(false);
	const [errorFlag, setErrorFlag] = useState<boolean>(false);
	const [errorMsg, setErrorMsg] = useState<string>("");
	const [algoIndex, setAlgoIndex] = useState<number>(0);
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
		axios
			.get("http://127.0.0.1:5000/algorithm", {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			})
			.then((response: Response) => {
				if ((response.status = statusOk)) {
					setAlgorithmNames([...response.data.result]);
				}
			})
			.catch((error) => {
				setErrorMsg(error.response.data);
				setErrorFlag(true);
				setLoader(false);
			});
	}, []);

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
	}, [file, algoFile, plcPath, plcSetPoint, pidValues, timeValue]);

	const sendQuery = () => {
		setLoader(true);
		let formData = new FormData();
		formData.append("file", file);
		formData.append("plcPath", JSON.stringify(plcPath));
		formData.append("pidValues", JSON.stringify({ ...pidValues }));
		formData.append("timeValue", JSON.stringify({ ...timeValue }));
		formData.append("setPoint", JSON.stringify({ plcSetPoint }));
		formData.append(
			"algorithm",
			JSON.stringify(algoFile?.name ?? algorithmNames[algoIndex])
		);
		if (algoFile) {
			formData.append("algorithmFile", algoFile);
		}

		axios
			.post("http://127.0.0.1:5000", formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			})
			.then((response) => {
				navigate("/output", {
					state: {
						pidBefore: {
							pVal: response.data.current_p,
							iVal: response.data.current_i,
							dVal: response.data.current_d,
						},
						pidAfter: {
							pVal: response.data.recommended_p,
							iVal: response.data.recommended_i,
							dVal: response.data.recommended_d,
						},
						setPoint: response.data.set_point,
						graphBefore: response.data.graph_before,
						graphAfter: response.data.graph_after,
					},
				});
			})
			.catch((error) => {
				setErrorMsg(error.response.data);
				setErrorFlag(true);
				setLoader(false);
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
	const onChangeAlgo = (e: any) => {
		setAlgoFile(e?.target?.files[0]);
	};

	return (
		<WidthContainer>
			{loader && <Loader />}
			{errorFlag && (
				<Error
					data={{
						errorMsg: errorMsg,
						errorFlag: errorFlag,
						errorToggle: errorToggle,
					}}
				/>
			)}
			<HeaderContainer>
				<H1Header>Server Query</H1Header>
			</HeaderContainer>
			<Algorithms algorithmIndex={setAlgoIndex} names={algorithmNames} />
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
							<InputFile
								type={"file"}
								id={"csvFileInput"}
								accept={".csv"}
								onChange={onChange}
							/>
							<DriveFolderUploadIcon />
							{" Upload CSV"}
						</Label>
						<Label>
							<InputFile
								type={"file"}
								id={"pyFileInput"}
								accept={".py"}
								onChange={onChangeAlgo}
							/>
							<DriveFolderUploadIcon />
							{" Upload Algorithm"}
						</Label>
					</Stack>
				</Stack>
			</Stack>
		</WidthContainer>
	);
};
