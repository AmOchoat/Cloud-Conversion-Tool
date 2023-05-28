import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomeScreen from "../components/HomeScreen";
import  React,{useContext} from 'react';
import { AuthContext } from '../context/auth-context';

import SignIn from "../components/SignIn";
import SignUp from "../components/SignUp";

const Routing = (props) => {
    const { isLoggedIn} = useContext(AuthContext);
    let routes;
    if (isLoggedIn) {
      routes = (
          <Routes>
            {/* la rutra por defecto es la de home */}
            <Route path="/home" exact element={<HomeScreen />}/>
            <Route path="*" element={<HomeScreen/>} />
          </Routes>
        );
      } else {
        routes = (
          <Routes>
            <Route path="/" exact element={<SignIn />}/>
            <Route path="/sign-up" exact element= {<SignUp />}/>
            <Route path="*" element={<SignIn/>} />
          </Routes>
        );
      }
    
   
    return(
        <BrowserRouter>
        {/* if (isLoggedIn) ir a /home */}
        
        
        
        {/* TODO: Realizar las rutas propias de la aplicación */ }

          {routes}

        </BrowserRouter>

    );
}

export default Routing;

