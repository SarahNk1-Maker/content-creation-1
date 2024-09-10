// src/components/Header.js
import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
//import { Link } from 'react-router-dom';
//import Logo from '../assets/logo.png'; // Adjust the path if needed

const Header = () => {
  return (
    <AppBar position="fixed" sx={{ backgroundColor: '#3c3c3c' }}>
      <Toolbar>
     
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Al@Math
        </Typography>
    <Button sx={{ color: 'white' }}>About Us</Button>
    <Button sx={{ color: 'white' }}>Blog</Button>
    <Button sx={{ color: 'white' }}>Contact</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;