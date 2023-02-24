import  React,{useState,useContext} from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Link as Link_Navigation} from 'react-router-dom'
import { green } from '@mui/material/colors';
import { AuthContext } from '../context/auth-context';

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://uniandes.edu.co/">
        ISIS 4426 - Desarrollo de Soluciones Cloud
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const theme = createTheme({
  palette: {
    primary: {
      main: green[600],
    },
  },
});

const SignUp =()=> {
  const { login } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    nombre: "",
    email: "",
    contrasena: "",
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevState) => ({ ...prevState, [name]: value }));
  };


  const handleSubmit = async (event) => {
    event.preventDefault();
    const formObject = new FormData(event.currentTarget);
    console.log({
      nombre:formObject.get('nombre'),
      password:formObject.get('password'),
      password_confirmation:formObject.get('password_confirmation'),
      email:formObject.get('password_confirmation')
    });
    const response = await fetch("http://127.0.0.1:5000/api/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre:formObject.get('nombre'),
        password:formObject.get('password'),
        password_confirmation:formObject.get('password_confirmation'),
        email:formObject.get('email')
      }),
    });
    const data = await response.json();
    console.log(data);
    login(data.access_token);
  }


  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: green[500] }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Registrarte
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
              margin="normal"
              required
              fullWidth
              id="nombre"
              label="Usuario"
              name="nombre"
              autoComplete="nombre"
              onChange={handleInputChange}
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Correo Electrónico"
              name="email"
              autoComplete="email"
              onChange={handleInputChange}
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Contraseña"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={handleInputChange}
            />
              <TextField
              margin="normal"
              required
              fullWidth
              name="password_confirmation"
              label="Confirmacion de contraseña"
              type="password_confirmation"
              id="password_confirmation"
              autoComplete="password_confirmation"
              onChange={handleInputChange}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Registrarte
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="#" variant="body2" component={Link_Navigation} to="/">
                  ¿Ya tienes una cuenta? Inicia Sesión
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 5 }} />
      </Container>
    </ThemeProvider>
  );
}
export default SignUp