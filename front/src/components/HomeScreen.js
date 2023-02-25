import  React,{useContext} from 'react';
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
import UploadForm from './UploadForm'

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
  const handleLogout = ()=>{}
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="relative">
        <Box style={{
          display:'flex', 
        justifyContent:'space-between',
        flexDirection:'row',
        }}>
          <CloudIcon sx={{ mr: 2 }} />
          <Typography variant="h6" color="white" noWrap>
            Cloud Conversion Tool
          </Typography>
          <Typography color="white" onClick={logout}>Sign out</Typography>
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
            <Typography variant="h5" align="center" color="text.secondary" paragraph>
                Esta herramienta completamente gratuita permite
                subir abiertamente diferentes formatos multimedia de 
                archivos y cambiarles su formato o realizar procesos de compresión.
            </Typography>
            <Stack
              sx={{ pt: 4 }}
              direction="row"
              spacing={2}
              justifyContent="center"
            >
              <UploadForm/>
              {/* <Button variant="contained">Subir un archivo</Button> */}
            </Stack>
          </Container>
        </Box>
        <Container sx={{ py: 8 }} maxWidth="md">
          {/* End hero unit */}
          <Grid container spacing={4}>
            {cards.map((card) => (
              <Grid item key={card} xs={12} sm={6} md={4}>
                <Card
                  sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
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
                    <Typography gutterBottom variant="h5" component="h2">
                      Nombre Archivo
                    </Typography>
                    <Typography>
                      Extensión archivo original
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small">Descargar</Button>
                    <Button size="small">Convertir</Button>
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