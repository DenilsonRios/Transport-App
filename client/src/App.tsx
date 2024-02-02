import { BrowserRouter, Routes, Route} from "react-router-dom";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import PassengerPage from "./pages/PassengerPage";
import DriverPage from "./pages/DriverPage";
import React from 'react';
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./ProtectedRoute";

function App(){
  return(
    <AuthProvider>
      <BrowserRouter>
        <Routes>
            <Route path='/' element = {<h1> Home page</h1>} />
            <Route path='/login' element = {<LoginPage/>} />
            <Route path='/register' element = {<RegisterPage/>} />
          <Route element = {<ProtectedRoute/>}>
            <Route path='/passenger' element = {<PassengerPage/>} />
            <Route path='/driver' element = {<DriverPage/>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}


export default App


