import {useForm }from 'react-hook-form'
import './RegisterPage.css'
import React, { useEffect } from 'react';
import {useAuth} from '../context/AuthContext'
import { useNavigate, Link } from 'react-router-dom';

function RegisterPage(){

    const {register, handleSubmit, formState:{errors}} = useForm();
    const {signup, isAuthenticated,user} = useAuth();
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
        signup(values);
    });

    return(

        <div id="contenedor">
            <div id="central">
                <div id="login">
                    <div className="titulo">
                       Register
                    </div>
                    <form onSubmit={onSubmit}>
                    <input type="text" {...register('user_name', {required: true})} placeholder="Username" className='input-field '/>
                    {errors.user_name && (<p className='text-red-500'>Nombre de usuario es requerido</p>)}
                    <input type="password" {...register('password', {required: true})} placeholder="Password" className='input-field  '/>
                    {errors.password && (<p className='text-red-500'>Contraseña es requerida</p>)}
                    <input type="text" {...register('name', {required: true})} placeholder="Name" className='input-field '/>
                    {errors.name && (<p className='text-red-500'>Nombre es requerido</p>)}
                    <input type="text" {...register('phone_number', {required: true})} placeholder="Phone" className='input-field  '/>
                    {errors.phone_number && (<p className='text-red-500'>Numero es requerido</p>)}
                    <label htmlFor="user_type" className="text-white">Tipo de usuario:</label>
                    <select {...register('user_type', { required: true })} id="user_type" className='select-field '>
                        <option value="driver">Conductor</option>
                        <option value="passenger">Pasajero</option>
                    </select>
                    <button type="submit" className='button-submit'>Crear</button>
                    </form>
                    <div className="pie-form">
                    <Link to="/login">Iniciar sesion</Link>
                    </div>
                </div>
                <div className="inferior">
                    
                </div>
            </div>
        </div>
    )
}

export default RegisterPage