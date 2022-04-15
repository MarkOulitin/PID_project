import React from "react";
import loaderGif from "./loader.gif";
import { MiddleScreenContainer } from "./utils.styled";

export default function Loader() {
	return (
		<MiddleScreenContainer>
			<img
				style={{ width: "300px", height: "300px" }}
				src={loaderGif}
				alt="loader-gif"
			/>
		</MiddleScreenContainer>
	);
}
