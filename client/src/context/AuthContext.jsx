import {createContext, useContext, useEffect, useState} from 'react';
import {registerRequest, loginRequest} from '../api/auth.js';
import Cookies from 'js-cookie'

export const AuthContext = createContext();

export const useAuth =  () =>{
    const context = useContext(AuthContext);
    if(!context){
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}

export const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null)
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const[errors, setErrors] = useState([]);


    const signup = async (user) => {
        try {

            let requestValues;
            if (user.user_type === 'passenger'){
                requestValues ={
                    ...user,
                    latitude : 0,
                    longitude: 0,
                    on_ride : 0
                }

            } else if (user.user_type === 'driver'){
                requestValues ={
                    ...user,
                    latitude : 0,
                    longitude: 0,
                    license_plate : null,
                    color: null,
                    availability: 1,
                }
            }

                
            const res = await registerRequest(requestValues)
            setUser(res.data);
            setIsAuthenticated(true);
            
        } catch (error) {
            setErrors(error.response.data)
        }
    };

    const signin = async (user) => {
        try {
            const res = await loginRequest(user);
            setUser(res.data)
            setIsAuthenticated(true);
            setHeaders(res.headers);
            console.log(res.headers);
        } catch (error) {
            setErrors([error.response.data])
        }

    
      
    useEffect(() => {
        const cookies = Cookies.get()
        if(cookies.token){
            console.log(cookies.token);
        }
    }, []);
        

    }; 
    return(
        <AuthContext.Provider  value={{
            signup,
            signin,
            user,
            isAuthenticated,
            errors,
        }}>
            {children}
        </AuthContext.Provider>
    )
} 