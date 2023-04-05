import React, { useContext } from 'react';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import CloudIcon from '@mui/icons-material/Cloud';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { green } from '@mui/material/colors';
import { AuthContext } from '../context/auth-context';
import UploadForm from './UploadForm';
import { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  Input,
  FormHelperText,
  TextField,
} from '@mui/material';

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {'Copyright © '}
      <Link color="inherit" href="https://uniandes.edu.co/">
        ISIS 4426 - Desarrollo de Soluciones Cloud
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

function download(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  // the filename you want
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

const cards = [1, 2, 3, 4, 5, 6, 7, 8, 9];

const theme = createTheme({
  palette: {
    primary: {
      main: green[500],
    },
  },
});

export default function HomeScreen() {
  const { logout } = useContext(AuthContext);
  const { accessToken } = useContext(AuthContext);

  const [max_tasks, setMaxTasks] = useState(5);
  const [order, setOrder] = useState(0);

  const [tasks, setTasks] = useState([]);

  // use effect para fetch de las tasks
  useEffect(() => {
    const formData = new FormData();
    formData.append('max_tasks', '5');
    formData.append('order', '0');

    fetch(
      `http://35.237.111.106:8000/api/tasks?max_tasks=${max_tasks}&order=${order}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    )
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log('Tasks:', data);

        setTasks(data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }, [max_tasks, order]);

  async function handleDescargar(id, name) {
    console.log('XD');

    fetch(`http://35.237.111.106:8000/api/files/${id}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((response) => {
        console.log(response);
        response.blob().then((blob) => download(blob, name));
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const handleLogout = () => {};

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="relative">
        <Box
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            flexDirection: 'row',
          }}
        >
          <CloudIcon sx={{ mr: 2 }} />
          <Typography variant="h6" color="white" noWrap>
            Cloud Conversion Tool
          </Typography>
          <Typography color="white" onClick={logout}>
            Sign out
          </Typography>
        </Box>
      </AppBar>
      <main>
        {/* Hero unit */}
        <Box
          sx={{
            bgcolor: 'background.paper',
            pt: 8,
            pb: 6,
          }}
        >
          <Container maxWidth="sm">
            <Typography
              component="h1"
              variant="h2"
              align="center"
              color="text.primary"
              gutterBottom
            >
              Cloud Conversion Tool
            </Typography>
            <Typography
              variant="h5"
              align="center"
              color="text.secondary"
              paragraph
            >
              Esta herramienta completamente gratuita permite subir abiertamente
              diferentes formatos multimedia de archivos y cambiarles su formato
              o realizar procesos de compresión.
            </Typography>
            <Stack
              sx={{ pt: 4 }}
              direction="row"
              spacing={2}
              justifyContent="center"
            >
              <UploadForm />
              {/* <Button variant="contained">Subir un archivo</Button> */}
            </Stack>
          </Container>
        </Box>

        <Container sx={{ py: 8 }} maxWidth="md">
          {/* End hero unit */}

          {/* Formulario con  */}
          <Box
            component="form"
            sx={{
              '& .MuiTextField-root': { m: 1, width: '25ch' },
            }}
            noValidate
            autoComplete="off"
          >
            <div>
              <TextField
                id="outlined-error"
                label="Max Tasks"
                defaultValue={5}
                onChange={(e) =>
                  setMaxTasks(e.target.value ? e.target.value : 5)
                }
              />
              <TextField
                id="outlined-error-helper-text"
                label="Orden"
                defaultValue={0}
                onChange={(e) => setOrder(e.target.value ? e.target.value : 0)}
              />
            </div>
          </Box>

          {/* Magin bot*/}
          <Box sx={{ pt: 4 }}></Box>

          <Grid container spacing={4}>
            {tasks?.map((task) => (
              <Grid item key={task} xs={12} sm={4} md={6}>
                <Card
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                  }}
                >
                  <CardMedia
                    component="img"
                    sx={{
                      // 16:9
                      pt: '56.25%',
                    }}
                    image="https://media.tenor.com/DiSK6Dwu0coAAAAC/tom-tom-meme.gif"
                    alt="random"
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography gutterBottom>
                      <strong>Nombre task: </strong>
                      {task.nombre}
                    </Typography>
                    <Typography>
                      <strong>archivo origen: </strong>
                      {task.nombre_archivo_ori}
                      {task.extension_original}
                    </Typography>
                    <Typography>
                      <strong>archivo destino: </strong>
                      {task.nombre_archivo_final}
                      {task.extension_convertir}
                    </Typography>
                    <Typography>
                      <strong>Fecha creacion: </strong>
                      {task.fecha}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      onClick={() =>
                        handleDescargar(
                          task.nombre_archivo_ori,
                          task.nombre_archivo_ori
                        )
                      }
                    >
                      Descargar
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </main>
      {/* Footer */}
      <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
        <Typography
          variant="subtitle1"
          align="center"
          color="text.secondary"
          component="p"
        >
          Proyecto de la clase - Entrega 1
        </Typography>
        <Copyright />
      </Box>
      {/* End footer */}
    </ThemeProvider>
  );
}
