
import {useForm }from 'react-hook-form'
import './RegisterPage.css'
import React, { useEffect } from 'react';
import {useAuth} from '../context/AuthContext'
import { useNavigate, Link} from 'react-router-dom';

function LoginPage(){

    const {register, handleSubmit, formState:{errors}} = useForm();
    const {signin,errors: signinErrors,isAuthenticated,user} = useAuth();
    const navigate = useNavigate();


    useEffect(() => {
        if (isAuthenticated) {
            if (user.user_type === 'passenger') {
                navigate('/passenger');
            } else if (user.user_type === 'driver') {
                navigate('/driver');
            }
        }  
    }, [isAuthenticated])

    const onSubmit = handleSubmit( async (values) => {
        signin(values);
    });

    return(

        <div id="contenedor">
            <div id="central">
                <div id="login">
                    <div className="titulo">
                        Login
                        {signinErrors.length === 1 && signinErrors[0].error === "UsersProfile matching query does not exist." && (
                        <div className='bg-red-500 p-2 text-white text-xs'>
                            Usuario o contraseña incorrecta
                        </div>
                        )}
                        {signinErrors.length === 1 && signinErrors[0].error === "Credenciales inválidas" && (
                        <div className='bg-red-500 p-2 text-white text-xs'>
                            Usuario o contraseña incorrecta
                        </div>
                        )}
                    </div>
                    <form onSubmit={onSubmit}>
                    <input type="text" {...register('user_name', {required: true})} placeholder="Username" className='input-field '/>
                    {errors.user_name && (<p className='text-red-500'>Nombre de usuario es requerido</p>)}
                    <input type="password" {...register('password', {required: true})} placeholder="Password" className='input-field  '/>
                    {errors.password && (<p className='text-red-500'>Contraseña es requerida</p>)}
                    <button type="submit" className='button-submit'>Ingresar</button>
                    </form>
                    <div className="pie-form">
                    <Link to="/register">Crear Cuenta</Link>
                    </div>
                </div>
                <div className="inferior">
                    
                </div>
            </div>
        </div>
    )
}

export default LoginPage