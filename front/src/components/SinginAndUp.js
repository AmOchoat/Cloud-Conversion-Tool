import React, { useState } from "react";
//import { SingIn, SingUp } from "../utilities/requests";
import { Link, useNavigate } from 'react-router-dom';


import "../styles/SinginAndUp.css"

function SinginAndUp(props) {
  // React States
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  // navigate
  const navigate = useNavigate();

 
  // Si props.modo = "in" entonces titulo = "Iniciar Sesión"
  // de lo contrario titulo = "Registrarse"
  const titulo = props.modo === "in" ? "Iniciar Sesión" : "Registrarse";

  // Si props.modo = "in" entonces vinculo = "Registrarse"
  // de lo contrario vinculo = "Iniciar Sesión"
  const vinculo = props.modo === "in" ? "singup" : "/";
  const tituloVinculo = props.modo === "in" ? "Registrarse" : "Iniciar Sesión";


  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error">{errorMessages.message}</div>
    );

  // JSX code for login form
  const renderForm = (
    <div className="form">
      <form onSubmit={function (){}}>
        <div className="input-container">
          <label>Correo </label>
          <input type="text" name="uname" required />
          {renderErrorMessage("uname")}
        </div>
        <div className="input-container">
          <label>Contraseña </label>
          <input type="password" name="pass" required />
          {renderErrorMessage("pass")}
        </div>
        <div className="button-container">
          <input type="submit" />
        </div>
        <div className="separator"></div>
        <div className="button-container">
          <Link to={vinculo}>{tituloVinculo}</Link>
        </div>
        
      </form>
    </div>
  );

  return (
    <div className="app">
      <div className="login-form">
        <div className="title">{titulo}</div>
        {isSubmitted ? <div>User is successfully logged in</div> : renderForm}
      </div>
    </div>
  );
}


export default SinginAndUp;