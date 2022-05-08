import styled from "styled-components";

export const HeaderContainer = styled.div`
	border:1px solid black;
	margin-top: 20px;
	display: flex;
	align-items: center;
	justify-content: center;
	text-align: center;
	width: 400px;
	height: 80px;
	border-radius: 15px 15px 15px 15px;
	background-color: white;
	margin-bottom: 30px;
`;

export const H1Header = styled.h1`
	font-size: 50px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
	color: black;
`;
export const H2Header = styled.h1`
	font-size: 30px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
	color: black;
`;
export const H2 = styled.h1`
	font-size: 25px;
	text-align: center;
	color: black;
`;
interface Temp {
	marginRight?: string;
}
export const H1 = styled.h1<Temp>`
	font-size: 30px;
	text-align: center;
	color: black;
	white-space: pre-line;
`;
export const H1Error = styled.h1<Temp>`
	font-size: 40px;
	text-align: center;
	color: #dc143c;
	white-space: pre-line;
`;
export const H2Error = styled.h1<Temp>`
	font-size: 20px;
	text-align: center;
	color: salmon;
	white-space: pre-line;
`;

export const MiddleScreenContainer = styled.div`
	position: fixed;
	top: 50%;
	left: 50%;
	-webkit-transform: translate(-50%, -50%);
	transform: translate(-50%, -50%);
	border-radius: 20% 20% 20% 20%;
	border: 1px solid black;
	background-color: #f0ffff;
	 z-index: 10;
`;

export const ErrorContainer = styled.div`
	padding: 10px 20px 10px 20px;
	border-radius: 20% 20% 20% 20%;
	border: 5px solid red;
	background-color: #232b2b;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
`;

export const ErrorButton = styled.button`
	width: 100px;
	height: 40px;
	border: 3px solid red;
	border-radius: 25% 25% 25% 25%;
	cursor: pointer;
	font-weight: bold;
	font: 15px;
`;
