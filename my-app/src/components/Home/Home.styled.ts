import styled from "styled-components";
import { Button as ButtonUI } from "@mui/material";

export const WidthContainer = styled.div`
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	border: black 5px solid;
	background-color: #f5f5dc;
	height: 100vh;
`;

export const Button = styled(ButtonUI)`
	&& {
		width: 400px;
		font-size: 30px;
		height: 50px;
		margin-top: 40px;
		margin-bottom: 20px;
	}
`;

export const InputFile = styled.input`
	display: none;
`;

export const Label = styled.label`
	display: inline-block;
	line-height: 45px;
	font-size: 30px;
	margin-top: 20px;
	margin-right:10px;
	border: 1px solid #ccc;
	display: inline-block;
	cursor: pointer;
	white-space: pre-wrap;
	text-align: center;
	font-weight: bold;
	color: white;
	border-radius: 10px;
	height: 50px;
	width: 300px;
	background-color: #1976d2;
`;

export const Span = styled.span`
	white-space: pre-wrap;
	font-weight: bold;
`;