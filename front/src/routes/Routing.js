import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomeScreen from "../components/HomeScreen";
import  React,{useContext} from 'react';
import { AuthContext } from '../context/auth-context';

import SignIn from "../components/SignIn";
import SignUp from "../components/SignUp";


const Routing = (props) => {
    const { isLoggedIn} = useContext(AuthContext);
    let routes;
    if(!isLoggedIn){
        routes=(
            <Routes>
                <Route exact path="/" element={<SignIn/>} />
                <Route exact path="/sign-up" element={<SignUp/>}/>
                <Route exact path="/home" element={<HomeScreen/>}/>
            </Routes>
        )
    }else{
        routes=(
            <Routes>
                <Route exact path="/" element={<HomeScreen/>} />
                <Route exact path="/sign-up" element={<SignUp/>}/>
                <Route exact path="/home" element={<HomeScreen/>}/>
            </Routes>
        )
    }
    
    return(
        <BrowserRouter>
                {/* TODO: Realizar las rutas propias de la aplicación */ }
                {routes}
        </BrowserRouter>

    );
}

export default Routing;

