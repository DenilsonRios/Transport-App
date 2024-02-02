import "./Formulario.css"
import {useState} from "react"

interface FormularioProps {
    setUserType: React.Dispatch<React.SetStateAction<string | null>>;
}


export function Formulario({setUserType}: FormularioProps){

    const [user_name, setName] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState(false)

    const handlerSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        if(user_name === "" || password === ""){
            setError(true)
            return
        }


        try {
            const response = await fetch("http://localhost:8000/transport/login/", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({user_name, password }),
            });
        
            if (!response.ok) {
              console.error("Error en la solicitud de inicio de sesión");
              return;
            }
            
        
            const data = await response.json();
            console.log('Respuesta del servidor:', data);
        
            const userType = data.user_type;
            
            setError(false)
            setUserType(userType);
        
        
          } catch (error) {
            console.error("Error al procesar la solicitud:", error);
          }
    }
    return(
        <section className="login-section">
            <h1 className="login-title">Login</h1>

            <form 
                className="formulario"
                onSubmit={handlerSubmit}
            >
                <input 
                    type = "text" 
                    value={user_name}
                    onChange={e => setName(e.target.value)}
                />
                <input 
                    type = "password" 
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
                <button>Iniciar sesion</button>
            </form>
            {error && <p>Todos los campos son obligatorios</p>}
        </section>
    )
}  


