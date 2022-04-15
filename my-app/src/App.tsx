import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Home } from "./components/Home/Home";
import { Output } from "./components/Output/Output";

function App() {
	return (
		<>
			<Router>
				<Routes>
					<Route path="/" element={<Home />} />
					<Route path="/output" element={<Output />} />
				</Routes>
			</Router>
		</>
	);
}

export default App;
