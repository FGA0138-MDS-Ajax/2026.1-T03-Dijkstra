import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../assets/css/login.css';
import logoSite from '../assets/img/logosite2.png';

const EnvelopeIcon = () => (<svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M20 4H4C2.9 4 2.01 4.9 2.01 6L2 18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4ZM20 8L12 13L4 8V6L12 11L20 6V8Z"/></svg>);
const LockIcon = () => (<svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M18 8H17V6C17 3.24 14.76 1 12 1C9.24 1 7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3C13.66 3 15 4.34 15 6V8H9V6ZM12 17C10.9 17 10 16.1 10 15C10 13.9 10.9 13 12 13C13.1 13 14 13.9 14 15C14 16.1 13.1 17 12 17Z"/></svg>);
const EyeIcon = () => (<svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M12 4.5C7 4.5 2.73 7.61 1 12C2.73 16.39 7 19.5 12 19.5C17 19.5 21.27 16.39 23 12C21.27 7.61 17 4.5 12 4.5ZM12 17C9.24 17 7 14.76 7 12C7 9.24 9.24 7 12 7C14.76 7 17 9.24 17 12C17 14.76 14.76 17 12 17ZM12 9C10.34 9 9 10.34 9 12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12C15 10.34 13.66 9 12 9Z"/></svg>);

export default function Login() {
    const [login, setLogin] = useState('');
    const [senha, setSenha] = useState('');
    const [error, setError] = useState(null);
    const [mostrarSenha, setMostrarSenha] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/api/login', { cpf: login, senha }, { withCredentials: true });
            if (response.data.success) {
                // CORREÇÃO AQUI: Converter de 'Administrador'/'Garçom' para 'ADMINISTRADOR'/'GARCOM'
                let cargoUsuario = response.data.data.cargo;
                cargoUsuario = cargoUsuario.toUpperCase().replace('Ç', 'C');
                
                localStorage.setItem('userCargo', cargoUsuario);
                
                if(cargoUsuario === 'ADMINISTRADOR') navigate('/produtos');
                else if(cargoUsuario === 'COZINHEIRO') navigate('/cozinha/fila');
                else navigate('/salao');
            }
        } catch (err) {
            setError(err.response?.data?.message || "Erro ao conectar com o servidor.");
        }
    };

    return (
        <div className="container-wrapper" style={{ display: 'flex', height: '100vh', width: '100vw', background: 'linear-gradient(300deg,rgba(0, 0, 0, 1) 13%, rgba(250, 0, 0, 1) 52%, rgba(0, 0, 0, 1) 90%)', justifyContent: 'center', alignItems: 'center' }}>
            <div className="container">
                 <img src={logoSite} alt="Logo Nexus Gourmet" className="logo" />
            </div>
            
            <div className="login">
                <nav className="login-nav">
                    <div className="login-header">
                        <h1 className="login-text">Olá!</h1>
                        <h2 className="login-text2">Faça Login em sua conta!</h2>
                    </div>
                    
                    <form onSubmit={handleLogin} style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        
                        <div className="input-container">
                            <div className="input-wrapper">
                                <span className="input-icon-left"><EnvelopeIcon /></span>
                                <input type="text" placeholder="Digite seu CPF (apenas números)" className="input-field" value={login} onChange={e => setLogin(e.target.value)} required />
                            </div>

                            <div className="input-wrapper">
                                <span className="input-icon-left"><LockIcon /></span>
                                <input type={mostrarSenha ? "text" : "password"} placeholder="Password" className="input-field" value={senha} onChange={e => setSenha(e.target.value)} required />
                                <span className="input-icon-right" onClick={() => setMostrarSenha(!mostrarSenha)}><EyeIcon /></span>
                            </div>
                        </div>

                        <div className="options">
                            <label className="remember-me">
                                <input type="checkbox" /> Remember me
                            </label>
                            <div className="forgot-password">
                                <a href="#">Forgot password?</a>
                            </div>
                        </div>
                        
                        {error && <div className="error-message">{error}</div>}

                        <button type="submit" className="login-button">SIGN IN</button>

                        <div className="signup-link">
                            Don't have an account? <a href="#">Create</a>
                        </div>

                    </form>
                </nav>
            </div>
        </div>
    );
}