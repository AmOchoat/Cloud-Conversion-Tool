import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomeScreen from "../components/HomeScreen";

import SignIn from "../components/SignIn";
import SignUp from "../components/SignUp";


const Routing = (props) => {
    return(
        <BrowserRouter>

            <Routes>
                {/* TODO: Realizar las rutas propias de la aplicación */ }
                <Route exact path="/" element={<SignIn/>} />
                <Route exact path="/sign-up" element={<SignUp/>}/>
                <Route exact path="/home" element={<HomeScreen/>}/>
            </Routes>

        </BrowserRouter>

    );
}

export default Routing;

