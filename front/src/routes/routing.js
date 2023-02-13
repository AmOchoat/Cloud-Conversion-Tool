import { BrowserRouter, Route, Routes } from "react-router-dom";
import SinginAndUp from "../components/SinginAndUp";


const Routing = (props) => {
    return(
        <BrowserRouter>

            <Routes>
                {/* TODO: Realizar las rutas propias de la aplicación */ }
                <Route exact path="/" element={<SinginAndUp modo = "in"/>} />
                <Route exact path="/singup" element={<SinginAndUp modo = "up"/>}/>
            </Routes>

        </BrowserRouter>

    );
}

export default Routing;

