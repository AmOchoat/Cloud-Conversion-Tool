import './App.css';
import Routing from "./routes/Routing";
import { AuthContext } from './context/auth-context';
import { useState, useCallback, useEffect } from 'react';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [accessToken, setAccessToken] = useState('');

  const login = useCallback(( accessToken) => {
 
    if(accessToken){
      console.log('entra')
      setIsLoggedIn(true);
      setAccessToken(accessToken);
      console.log(accessToken)
      localStorage.setItem('userData', JSON.stringify({ accessToken }));
    }
   
  }, []);
  const logout = useCallback(() => {
    setIsLoggedIn(false);
    setAccessToken('');
    localStorage.removeItem('userData');
  }, []);

  useEffect(() => {
    const userData = localStorage.getItem('userData');
    if (userData) {
      const storedData = JSON.parse(userData);
      if (storedData && storedData.accessToken) {
        login(storedData.userId, storedData.accessToken);
      }
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        isLoggedIn,
        login,
        logout,
        accessToken,
        setAccessToken,
      }}
    > <Routing sesion ="in"/>
    </AuthContext.Provider>
     
  );
}

export default App;
